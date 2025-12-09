from __future__ import annotations
from pydantic import BaseModel, Field
from models.models import Detail


class DetailSchema(BaseModel):
    """Detail input/output for title and description."""
    title: str = Field(..., description="Title of the entity must be unique (length constraints in Service layer)")
    description: str = Field(..., description="Description of the entity (length constraints in Service layer)")

    @classmethod
    def from_detail(cls, detail: Detail) -> DetailSchema:
        return cls(
            title=detail.title,
            description=detail.description
        )