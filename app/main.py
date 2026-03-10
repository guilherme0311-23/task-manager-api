from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base
from .schemas import Task, TaskCreate, TaskUpdate
from . import storage

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
def list_tasks(db: Session = Depends(get_db)):
    return storage.list_tasks(db)

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = storage.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    return storage.create_task(db, payload)

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = storage.update_task(db, task_id, payload)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    ok = storage.delete_task(db, task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return None

@app.patch("/tasks/{task_id}/done", response_model=Task)
def toggle_done(task_id: int, db: Session = Depends(get_db)):
    task = storage.toggle_done(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task