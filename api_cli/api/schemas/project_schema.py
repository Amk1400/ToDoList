from typing import List
from pydantic import BaseModel
from api_cli.api.schemas.detail_schema import DetailBase
from api_cli.api.schemas.task_schema import TaskResponse


class ProjectBase(BaseModel):
    detail: DetailBase


class ProjectCreate(BaseModel):
    title: str
    description: str


class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class ProjectResponse(ProjectBase):
    id: int
    tasks: List[TaskResponse] = []

    class Config:
        from_attributes = True