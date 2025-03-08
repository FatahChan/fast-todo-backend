import tomllib
from importlib.resources import files
from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import todos
from fastapi.middleware.cors import CORSMiddleware

# Read project metadata from pyproject.toml using package root
pyproject_path = files("app").parent / "pyproject.toml"
with open(pyproject_path, "rb") as f:
    pyproject = tomllib.load(f)

app = FastAPI(
    title=pyproject["project"]["name"],
    version=pyproject["project"]["version"],
    description=pyproject["project"]["description"],
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(todos.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
