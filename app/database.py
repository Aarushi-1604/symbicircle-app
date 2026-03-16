import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# loading environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# creating connection to neon
engine = create_engine(DATABASE_URL)

# creating session factory that handles individual database tasks
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# creating Base class
Base = declarative_base()

# helper function to get db connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
