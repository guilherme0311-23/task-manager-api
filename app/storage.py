from typing import List, Optional
from sqlalchemy.orm import Session
from .models import TaskModel, UserModel
from .schemas import TaskCreate, TaskUpdate, UserCreate
from .security import hash_password


def list_tasks(db: Session, user_id: int) -> List[TaskModel]:
    return (
        db.query(TaskModel)
        .filter(TaskModel.owner_id == user_id)
        .order_by(TaskModel.id)
        .all()
    )


def get_task(db: Session, task_id: int, user_id: int) -> Optional[TaskModel]:
    return (
        db.query(TaskModel)
        .filter(TaskModel.id == task_id, TaskModel.owner_id == user_id)
        .first()
    )


def create_task(db: Session, data: TaskCreate, user_id: int) -> TaskModel:
    task = TaskModel(
        title=data.title,
        description=data.description,
        done=False,
        owner_id=user_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task_id: int, data: TaskUpdate, user_id: int) -> Optional[TaskModel]:
    task = get_task(db, task_id, user_id)
    if not task:
        return None

    payload = data.model_dump(exclude_none=True)
    for k, v in payload.items():
        setattr(task, k, v)

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, user_id: int) -> bool:
    task = get_task(db, task_id, user_id)
    if not task:
        return False

    db.delete(task)
    db.commit()
    return True


def toggle_done(db: Session, task_id: int, user_id: int) -> Optional[TaskModel]:
    task = get_task(db, task_id, user_id)
    if not task:
        return None

    task.done = not task.done
    db.commit()
    db.refresh(task)
    return task


def get_user_by_email(db: Session, email: str) -> Optional[UserModel]:
    return db.query(UserModel).filter(UserModel.email == email).first()


def create_user(db: Session, data: UserCreate) -> UserModel:
    user = UserModel(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user:
        return None

    from .security import verify_password

    if not verify_password(password, user.password_hash):
        return None

    return user