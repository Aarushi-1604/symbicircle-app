from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..utils.security import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(tags = ["Authentication"])

@router.post ("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    #Checking if email is already in database
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Email already registered"
        )
    # Hashing the user's password
    hashed_pass = hash_password(user.password)

    # Creating the database record
    new_user = models.User(
        full_name = user.full_name,
        email=user.email,
        hashed_password=hashed_pass,
        branch=user.branch,
        batch=user.batch
    )

    # Saving and refresh
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login_user(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    # 1. Find the user by email (OAuth2Form uses 'username' field for email)
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # 2. If user doesn't exist or password doesn't match
    if not user or not verify_password(user_credentials.password, str(user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    # 3. Create the "Digital ID Card" (JWT)
    access_token = create_access_token(data={"sub": user.email})

    # 4. Return the token
    return {"access_token": access_token, "token_type": "bearer"}

# Add get_current_user to your imports at the top
from ..utils.security import verify_password, create_access_token, get_current_user

@router.get("/me", response_model=schemas.UserOut)
def get_user_profile(current_user: models.User = Depends(get_current_user)):
    """
    This route is protected. Only users with a valid JWT can see their info.
    """
    return current_user