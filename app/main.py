from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import todos

app = FastAPI()


app.include_router(todos.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
