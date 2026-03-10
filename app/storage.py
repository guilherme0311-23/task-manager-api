from typing import List, Optional
from sqlalchemy.orm import Session
from .models import TaskModel
from .schemas import TaskCreate, TaskUpdate

def list_tasks(db: Session) -> List[TaskModel]:
    return db.query(TaskModel).order_by(TaskModel.id).all()

def get_task(db: Session, task_id: int) -> Optional[TaskModel]:
    return db.query(TaskModel).filter(TaskModel.id == task_id).first()

def create_task(db: Session, data: TaskCreate) -> TaskModel:
    task = TaskModel(title=data.title, description=data.description, done=False)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task(db: Session, task_id: int, data: TaskUpdate) -> Optional[TaskModel]:
    task = get_task(db, task_id)
    if not task:
        return None

    payload = data.model_dump(exclude_none=True)
    for k, v in payload.items():
        setattr(task, k, v)

    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int) -> bool:
    task = get_task(db, task_id)
    if not task:
        return False

    db.delete(task)
    db.commit()
    return True

def toggle_done(db: Session, task_id: int) -> Optional[TaskModel]:
    task = get_task(db, task_id)
    if not task:
        return None

    task.done = not task.done
    db.commit()
    db.refresh(task)
    return task