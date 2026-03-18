from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routes import auth

models.Base.metadata.create_all(bind = engine)
app = FastAPI(title="SymbiCircle")

# Including routers
app.include_router(auth.router)

@app.get("/")
def home():
    return {"message":"SymbiCircle API is live!", "version":"0.2.0"}