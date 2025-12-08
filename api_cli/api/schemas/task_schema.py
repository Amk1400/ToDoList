from datetime import date
from pydantic import BaseModel
from api_cli.api.schemas.detail_schema import DetailBase


class TaskBase(BaseModel):
    detail: DetailBase


class TaskCreate(BaseModel):
    title: str
    description: str
    deadline: date | None = None
    status: str = "todo"


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    deadline: date | None = None
    status: str | None = None


class TaskResponse(TaskBase):
    id: int
    deadline: date | None = None
    status: str
    closed_at: date | None = None

    class Config:
        from_attributes = True