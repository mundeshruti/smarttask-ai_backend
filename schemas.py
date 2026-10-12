
from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Priority = Literal["Low", "Medium", "High"]


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    priority: Priority = "Medium"
    due_date: date | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None, min_length=1, max_length=200
    )
    description: str | None = None
    priority: Priority | None = None
    due_date: date | None = None
    completed: bool | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    priority: str
    due_date: date | None
    completed: bool

    model_config = ConfigDict(from_attributes=True)
