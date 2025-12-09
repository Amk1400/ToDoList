from datetime import date, datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field
from api_cli.api.schemas.detail_schema import DetailSchema


class TaskResponse(BaseModel):
    """Task response output."""
    id: Optional[int]
    project_id: int
    detail: DetailSchema
    status: Optional[Literal["todo", "doing", "done"]] = (
        Field(..., description="Task status; must be one of 'todo', 'doing', 'done'"))
    deadline: date = Field(..., description="Deadline in format YYYY-MM-DD; must not be in the past")
    closed_at: datetime | None = None
