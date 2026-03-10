from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    done: bool | None = None

class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    done: bool
    created_at: datetime

    class Config:
        from_attributes = True