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
            query = query.filter(models.User.skills).filter(models.Skill.name.ilike(skill))

    return query.distinct().all()

@router.get("/skills/suggest", response_model=List[str])
def suggest_skills(q: str = Query(..., min_length=1), db: Session = Depends(database.get_db)):
    """
    The 'Type-Ahead' Logic:
    When user types 'Py', returns ['Python', 'PyTorch', etc.]
    """
    skills = db.query(models.Skill).filter(models.Skill.name.ilike(f"{q}%")).limit(10).all()
    return [skill.name for skill in skills]