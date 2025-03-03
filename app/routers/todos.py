from fastapi import APIRouter, HTTPException, Query
from typing import Annotated
from app.database import SessionDep
from app.models.todo import Todo
from sqlmodel import select


router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)


@router.post("/todos")
async def create_todo(session: SessionDep, todo: Todo):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@router.get("/todos")
async def get_todos(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    todos = session.exec(select(Todo).offset(offset).limit(limit)).all()
    return todos


@router.get("/todos/{todo_id}")
async def get_todo_by_id(session: SessionDep, todo_id: int):
    todo = session.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


async def edit_todo_by_id(session: SessionDep, todo_id: int, todo: Todo):
    todo = session.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.name = todo.name
    todo.completed = todo.completed
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@router.delete("/todos/{todo_id}")
async def delete_todo_by_id(session: SessionDep, todo_id: int):
    todo = session.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return
