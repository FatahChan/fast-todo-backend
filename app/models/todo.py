from sqlmodel import Field, SQLModel


class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    completed: bool = Field(default=False)
