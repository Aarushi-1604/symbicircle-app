from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.security import OAuth2PasswordRequestForm

from .. import models, schemas, database
from ..utils.security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # 1. Check if email exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Initialize User object
    hashed_pass = hash_password(user.password)
    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_pass,
        branch=user.branch,
        batch=user.batch
    )

    # Add user to session so we can start attaching skills
    db.add(new_user)

    # 3. Handle Skills (The "Smart Link")
    for skill_name in user.skills:
        skill_name_clean = skill_name.strip().title()

        # Check if skill exists
        db_skill = db.query(models.Skill).filter(models.Skill.name.ilike(skill_name_clean)).first()

        if not db_skill:
            # Create it if it doesn't exist
            db_skill = models.Skill(name=skill_name_clean)
            db.add(db_skill)
            # We don't commit yet! Just add it to the session.

        # Link the skill to the user's relationship collection
        new_user.skills.append(db_skill)

    # 4. Final Transaction (Atomic)
    try:
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        print(f"Registration Error: {e}")
        raise HTTPException(status_code=500, detail="Database error during registration")

    return new_user


@router.post("/login", response_model=schemas.Token)
def login_user(
        user_credentials: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(database.get_db)
):
    # Find user by email (OAuth2Form uses 'username' field)
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        print(f"DEBUG: User {user_credentials.username} not found in database.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    # Verify password (removed the str() cast which can cause issues with some hashers)
    is_password_correct = verify_password(user_credentials.password, user.hashed_password)

    if not is_password_correct:
        print(f"DEBUG: Password verification failed for user {user.email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    # If everything is correct, create the token
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserOut)
def get_user_profile(current_user: models.User = Depends(get_current_user)):
    """
    Protected route to fetch current logged-in user data.
    """
    return current_user