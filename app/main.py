from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routes import auth

models.Base.metadata.create_all(bind = engine)
app = FastAPI(
    title="SymbiCircle",
    version="0.2.0",
)

# This is what makes the "Authorize" button appear!
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def home():
    return {"message": "Welcome to SymbiCircle API"}