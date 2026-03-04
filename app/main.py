from fastapi import FastAPI, HTTPException
from .schemas import Task, TaskCreate
from . import storage

app = FastAPI(title="Task Manager API")

@app.get("/")
def root():
    return {"status": "ok", "message": "Task Manager API no ar 🚀"}

@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return storage.list_tasks()

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = storage.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate):
    return storage.create_task(payload)