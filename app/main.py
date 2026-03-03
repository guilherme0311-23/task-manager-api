from fastapi import FastAPI

app = FastAPI(title="Task Manager API")

@app.get("/")
def root():
    return {"status": "ok", "message": "Task Manager API no ar 🚀"}