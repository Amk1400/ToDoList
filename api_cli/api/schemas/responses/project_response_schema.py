from typing import Optional
from pydantic import BaseModel

from api_cli.api.schemas.detail_schema import DetailSchema


class ProjectResponse(BaseModel):
    """Project response output."""
    id: Optional[int]
    detail: DetailSchema