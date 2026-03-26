from fastapi import FastAPI, Request
from .database import engine, Base
from . import models
from .routes import auth,users
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
models.Base.metadata.create_all(bind = engine)
app = FastAPI(
    title="SymbiCircle",
    version="0.2.0",
)


app.include_router(auth.router, prefix="/auth")
app.include_router(users.router)
@app.get("/")
def home():
    return {"message": "Welcome to SymbiCircle API"}\

app.mount("/static",StaticFiles(directory="app/static"),name="static")

templates = Jinja2Templates(directory="app/templates")

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@app.get("/register/skills")
async def register_skills_page(request: Request):
    return templates.TemplateResponse("auth/register_skills.html", {"request": request})