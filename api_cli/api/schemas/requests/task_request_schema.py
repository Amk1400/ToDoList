from datetime import date, datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field, validator

from api_cli.api.schemas.detail_schema import DetailSchema


class TaskRequest(BaseModel):
    """Task input schema."""
    detail: DetailSchema
    status: Optional[Literal["todo", "doing", "done"]] = Field(
        None, description="Task status; must be one of 'todo', 'doing', 'done' default is last value"
    )
    deadline: date = Field(
        ..., description="Deadline in format YYYY-MM-DD; must not be in the past"
    )


class TaskCreate(TaskRequest):
    """Task creation input."""
    status: Optional[Literal["todo", "doing", "done"]] = Field(
        "todo", description="Task status; must be one of 'todo', 'doing', 'done'; default is 'todo'"
    )


class TaskUpdate(TaskRequest):
    """Task update input."""