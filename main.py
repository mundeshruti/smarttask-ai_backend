import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from openai import APIError, RateLimitError

from database import Base, engine, get_db
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskResponse
from ai_schemas import (
    ImproveDescriptionRequest,
    ImproveDescriptionResponse,
)
from ai_service import improve_task_description


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="SmartTask AI API",
    description="Task management API for SmartTask AI",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "SmartTask AI API is running"}


# Get all tasks
@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).order_by(Task.id.desc()).all()


# Create a task
@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    task = Task(**data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


# Update a task
# @app.put("/tasks/{task_id}", response_model=TaskResponse)
# def update_task(
#     task_id: int,
#     data: TaskUpdate,
#     db: Session = Depends(get_db),
# ):
#     task = db.get(Task, task_id)

#     if task is None:
#         raise HTTPException(status_code=404, detail="Task not found")

#     changes = data.model_dump(exclude_unset=True)

#     for key, value in changes.items():
#         setattr(task, key, value)

#     db.commit()
#     db.refresh(task)
#     return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    updates = task_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task

# Delete a task
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return Response(status_code=204)


# AI: Improve task description

@app.post(
    "/ai/improve-task-description",
    response_model=ImproveDescriptionResponse,
)
def improve_description(data: ImproveDescriptionRequest):
    title = data.title.strip()

    if not title:
        raise HTTPException(
            status_code=422,
            detail="Task title cannot be empty.",
        )

    try:
        description = improve_task_description(
            title=title,
            notes=data.notes.strip(),
        )
        return ImproveDescriptionResponse(description=description)

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc
