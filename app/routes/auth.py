from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..utils.security import hash_password

router = APIRouter(prefix="/auth", tags = ["Authentication"])

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
