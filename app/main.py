import tomllib
from importlib.resources import files
from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import todos

# Read project metadata from pyproject.toml using package root
pyproject_path = files("app").parent / "pyproject.toml"
with open(pyproject_path, "rb") as f:
    pyproject = tomllib.load(f)

app = FastAPI(
    title=pyproject["project"]["name"],
    version=pyproject["project"]["version"],
    description=pyproject["project"]["description"],
)

app.include_router(todos.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
