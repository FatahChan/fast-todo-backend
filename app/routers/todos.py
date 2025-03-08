from fastapi import APIRouter, HTTPException, Query
from typing import Annotated
from app.database import SessionDep
from app.models.todo import Todo
from sqlmodel import select, SQLModel


class TodoCreate(SQLModel):
    name: str

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def create_todo(session: SessionDep, todo: TodoCreate) -> Todo:
    db_todo = Todo(name=todo.name, completed=False)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@router.get("/")
async def get_todos(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Todo]:
    todos = session.exec(select(Todo).offset(offset).limit(limit)).all()
    return todos


@router.get("/{todo_id}")
async def get_todo_by_id(session: SessionDep, todo_id: int) -> Todo:
    todo = session.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}")
async def edit_todo_by_id(session: SessionDep, todo_id: int, todo: Todo) -> Todo:
    db_todo = session.get(Todo, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.name = todo.name
    db_todo.completed = todo.completed
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@router.delete("/{todo_id}")
async def delete_todo_by_id(session: SessionDep, todo_id: int):
    todo = session.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return
