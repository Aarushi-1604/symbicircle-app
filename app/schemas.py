from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List


# Defining what user must send to register
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(...,min_length=8)
    branch: str
    batch: str
    skills: List[str] = Field(..., json_schema_extra={
        'example': ['Python', 'FastAPI', 'NLP', 'Machine Learning', 'PostgreSQL']})

    @field_validator('email')
    @classmethod
    def validate_sit_email(cls,v:str) -> str:
        # Needs to match the firstname.lastname.btech202X@sitpune.edu.in
        if not v.endswith("@sitpune.edu.in"):
            raise ValueError('Only SIT Pune email addresses are allowed')
        return v.lower()
    @field_validator('skills')
    @classmethod
    def validate_minimum_skills(cls, v):
        # Removing duplicates and empty strings
        unique_skills = list(set([s.strip() for s in v if s.strip()]))

        # Enforcing the minimum 5 skills rule
        if len(unique_skills) < 5:
            raise ValueError("You must select at least 5 mandatory skills to join SymbiCircle")
        return unique_skills


class SkillOut(BaseModel):
    name: str
    class Config:
        from_attributes = True
# Data going OUT
class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    branch: str
    batch: str
    skills: List[SkillOut] = []
    # is_verified: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None