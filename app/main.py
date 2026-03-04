from fastapi import FastAPI, HTTPException
from .schemas import Task, TaskCreate, TaskUpdate
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

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate):
    task = storage.update_task(task_id, payload)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    ok = storage.delete_task(task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return None

@app.patch("/tasks/{task_id}/done", response_model=Task)
def toggle_done(task_id: int):
    task = storage.toggle_done(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task