from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# table connecting Users to Skills (Many to Many)
user_skills = Table(
    "user_skills",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String,nullable=False)
    email= Column(String,unique=True, index= True,nullable=False)
    hashed_password = Column(String,nullable=False)
    branch = Column(String)
    batch = Column(String)
    is_verified = Column(Boolean, default=False)
    skills = relationship("Skill", secondary=user_skills, back_populates="users")

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=False, unique=True, index=True)
    users = relationship("User", secondary=user_skills, back_populates="skills")