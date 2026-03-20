from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..utils.security import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(tags = ["Authentication"])


@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # 1. Standard email check
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Create the User object (without skills yet)
    hashed_pass = hash_password(user.password)
    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_pass,
        branch=user.branch,
        batch=user.batch
    )
    db.add(new_user)
    # 3. Handle the "Crowdsourced" Skills
    for skill_name in user.skills:
        # Check if skill exists (Case-insensitive)
        db_skill = db.query(models.Skill).filter(models.Skill.name.ilike(skill_name)).first()

        if not db_skill:
            # If it's a new skill, add it to the Master List
            db_skill = models.Skill(name=skill_name.title())
            db.add(db_skill)
            db.commit()
            db.refresh(db_skill)

        # Link the skill to the user
        new_user.skills.append(db_skill)

    # 4. Save User (and the links in the association table)
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