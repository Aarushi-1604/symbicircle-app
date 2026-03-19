from pydantic import BaseModel, EmailStr
from typing import Optional, List

# Defining what user must send to register
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    branch: str
    batch: str

# Data going OUT
class UserOut(BaseModel):
    id : int
    full_name: str
    email: EmailStr
    branch: str
    batch:str
    is_verified: bool
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None