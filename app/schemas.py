from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

class Task(TaskCreate):
    id: int
    done: bool = False
    created_at: datetime