from __future__ import annotations
from pydantic import BaseModel

from api_cli.api.schemas.detail_schema import DetailSchema


class ProjectRequest(BaseModel):
    """Project creation input."""
    detail: DetailSchema


class ProjectCreate(ProjectRequest):
    """Project creation input."""

class ProjectUpdate(ProjectRequest):
    """Project update input."""



