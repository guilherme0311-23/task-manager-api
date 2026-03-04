from datetime import datetime
from typing import List, Optional
from .schemas import Task, TaskCreate

_tasks: List[Task] = []
_next_id = 1

def list_tasks() -> List[Task]:
    return _tasks

def get_task(task_id: int) -> Optional[Task]:
    for t in _tasks:
        if t.id == task_id:
            return t
    return None

def create_task(data: TaskCreate) -> Task:
    global _next_id
    task = Task(
        id=_next_id,
        title=data.title,
        description=data.description,
        done=False,
        created_at=datetime.utcnow(),
    )
    _tasks.append(task)
    _next_id += 1
    return task