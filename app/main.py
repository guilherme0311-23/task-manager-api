from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from .database import SessionLocal, engine, Base
from .schemas import (
    Task,
    TaskCreate,
    TaskUpdate,
    User,
    UserCreate,
    LoginRequest,
    Token
)
from . import storage
from .security import create_access_token, get_current_user
from .models import UserModel

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"status": "ok", "message": "Task Manager API no ar 🚀"}


@app.get("/tasks", response_model=list[Task])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return storage.list_tasks(db, current_user.id)


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    task = storage.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return storage.create_task(db, payload, current_user.id)


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    task = storage.update_task(db, task_id, payload, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    ok = storage.delete_task(db, task_id, current_user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return None


@app.patch("/tasks/{task_id}/done", response_model=Task)
def toggle_done(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    task = storage.toggle_done(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/users", response_model=User, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing_user = storage.get_user_by_email(db, payload.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return storage.create_user(db, payload)

@app.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = storage.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }