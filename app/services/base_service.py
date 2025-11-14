from abc import ABC
from typing import Generic, TypeVar
from app.models.models import Detail

T = TypeVar("T")


class BaseManager(ABC, Generic[T]):
    """Base manager providing validation helpers only."""

    def __init__(self, config) -> None:
        """Initialize with configuration."""
        self._config = config

    def _validate_detail(self, detail: Detail, max_title: int, max_description: int) -> None:
        """Validate title and description lengths.

        Args:
            detail (Detail): Detail to validate.
            max_title (int): Maximum title length.
            max_description (int): Maximum description length.

        Raises:
            ValueError: If title or description exceed limits.
        """
        if not detail.title or len(detail.title) > max_title:
            raise ValueError(f"Title must be 1-{max_title} chars")
        if not detail.description or len(detail.description) > max_description:
            raise ValueError(f"Description must be 1-{max_description} chars")
