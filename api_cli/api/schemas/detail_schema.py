from __future__ import annotations
from pydantic import BaseModel, Field
from models.models import Detail


class DetailSchema(BaseModel):
    """Detail input/output for title and description."""
    title: str = Field(..., description="Title of the entity must be unique (length constraints in Service layer)")
    description: str = Field(..., description="Description of the entity (length constraints in Service layer)")

    def __init__(self, detail: Detail):
        super().__init__()
        self.title = detail.title
        self.description = detail.description
