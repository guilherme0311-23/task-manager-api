from datetime import datetime
from typing import List, Optional
from .schemas import Task, TaskCreate, TaskUpdate

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

def update_task(task_id: int, data: TaskUpdate) -> Optional[Task]:
    task = get_task(task_id)
    if not task:
        return None

    updated = task.model_copy(
        update={
            k: v for k, v in data.model_dump().items() if v is not None
        }
    )

    # troca na lista
    for i, t in enumerate(_tasks):
        if t.id == task_id:
            _tasks[i] = updated
            break

    return updated

def delete_task(task_id: int) -> bool:
    global _tasks
    before = len(_tasks)
    _tasks = [t for t in _tasks if t.id != task_id]
    return len(_tasks) < before

def toggle_done(task_id: int) -> Optional[Task]:
    task = get_task(task_id)
    if not task:
        return None

    updated = task.model_copy(update={"done": not task.done})

    for i, t in enumerate(_tasks):
        if t.id == task_id:
            _tasks[i] = updated
            break

    return updated