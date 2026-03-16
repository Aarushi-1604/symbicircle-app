from fastapi import FastAPI
from .database import engine, Base
from . import models

models.Base.metadata.create_all(bind = engine)
app = FastAPI(title="SymbiCircle")
@app.get("/")
def home():
    return{"message":"SymbiCircle API is live!","database": "Connected"}