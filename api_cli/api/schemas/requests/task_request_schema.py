from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

from api_cli.api.schemas.detail_schema import DetailSchema
from models.models import Status


class TaskRequest(BaseModel):
    """Task input schema."""
    detail: DetailSchema
    status: Optional[Status] = Field(
        None, description="Task status; must be one of 'todo', 'doing', 'done' default is last value"
    )
    deadline: date = Field(
        ..., description="Deadline in format YYYY-MM-DD; must not be in the past"
    )


class TaskCreate(TaskRequest):
    """Task creation input."""
    status: Optional[Status] = Field(
        "todo", description="Task status; must be one of 'todo', 'doing', 'done'; default is 'todo'"
    )


class TaskUpdate(TaskRequest):
    """Task update input."""