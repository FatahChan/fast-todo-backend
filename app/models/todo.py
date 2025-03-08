from sqlmodel import Field, SQLModel, select
from datetime import datetime
from typing import Annotated
from pydantic import StringConstraints

TodoPublicId = Annotated[str, StringConstraints(pattern=r"^TD-\d{6}\\d{4}$")]

def generate_public_id():
    from app.database import get_session  # Import here to avoid circular imports
    
    prefix = f"TD-{datetime.now():%Y%m}"
    with get_session() as session:
        # Get latest todo for current month
        latest = session.exec(
            select(Todo)
            .where(Todo.public_id.like(f"{prefix}%"))
            .order_by(Todo.public_id.desc())
        ).first()
        
        if not latest:
            return f"{prefix}0001"
            
        current_number = int(latest.public_id.split("-")[1][6:])  # Extract the number part
        return f"{prefix}{str(current_number + 1).zfill(4)}"  # Pad with zeros

class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    public_id: TodoPublicId  = Field(
        default_factory=generate_public_id,
        unique=True,
        index=True,
        description="Public ID of the todo, format with TD-YYYYMMXXXX",
        regex=r"^TD-\d{6}\\d{4}$"
    )
    name: str = Field(index=True)
    completed: bool = Field(default=False)