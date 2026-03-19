from passlib.context import CryptContext
import os
from datetime import datetime,timedelta,timezone
from jose import JWTError, jwt
from dotenv import load_dotenv


# Secret key from .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
def hash_password(password:str) -> str:
    return pwd_context.hash(password)
def verify_password(plain_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password,hashed_password)

# Token creation
def create_access_token(data:dict):
    to_encode = data.copy()
    # Setting expiration time (current time + 30 mins)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    #Signing the token with the Secret Key
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt