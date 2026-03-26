from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, database

router = APIRouter(prefix = "/users",tags=["User Discovery"])

@router.get("/search",response_model=List[schemas.UserOut])
def search_users(
        branch: Optional[str] = Query(None, description="Filter by Branch"),
        skill_query: Optional[str] = Query(None, description="Comma-separated skills"),
        db: Session = Depends(database.get_db)
):
    """
    Dynamic Search: Filters by branch and skills.
    If you send 'Python, FastAPI', it finds users who have BOTH.
    """
    query = db.query(models.User)
    # Filter by Branch
    if branch:
        query = query.filter(models.User.branch.ilike(branch))

    # Filter by skills
    if skill_query:
        # cleaning the input eg. "ml,fastapi" -> ["ML","Fastapi"]
        search_skills = [s.strip().title() for s in skill_query.split(",")]

        # ensuring the user has EVERY skill requested
        for skill in search_skills:
            query=query.filter(models.User.skills.any(models.Skill.name.ilike(skill)))
    return query.distinct().all()

@router.get("/skills/suggest", response_model=List[str])
def suggest_skills(q: str = Query(..., min_length=1), db: Session = Depends(database.get_db)):
    """
    The 'Type-Ahead' Logic:
    When user types 'Py', returns ['Python', 'PyTorch', etc.]
    """
    skills = db.query(models.Skill).filter(models.Skill.name.ilike(f"{q}%")).limit(10).all()
    return [skill.name for skill in skills]

@router.get("/search", response_model=List[schemas.UserOut])
def search_students(
    branch: Optional[str] = None,
    skill_query: Optional[str] = None,
    db: Session = Depends(database.get_db)
):
    # Start with all users
    query = db.query(models.User)

    # 1. Filter by Branch (Exact match)
    if branch:
        query = query.filter(models.User.branch == branch)

    # 2. Filter by Skill (Partial match/Case-insensitive)
    if skill_query:
        # We join the Skill table so we can filter based on the skill name
        query = query.join(models.User.skills).filter(
            models.Skill.name.ilike(f"%{skill_query}%")
        )

    # .distinct() ensures that if a user matches multiple skills,
    # they only appear once in the results.
    return query.distinct().all()