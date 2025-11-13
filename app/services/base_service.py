from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List
from app.models.models import Detail, Status
from app.core.config import AppConfig
from app.exceptions.entity import NotFoundError

T = TypeVar("T")


class BaseManager(ABC, Generic[T]):
    """Generic base manager providing core CRUD and validation."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize with configuration."""
        self._config: AppConfig = config

    def create(self, items: List[T], detail: Detail) -> None:
        """Append a new item after validation."""
        self._validate(detail)
        items.append(self._create(items, detail))

    def get(self, items: List[T], index: int) -> T:
        """Retrieve item by index."""
        if not (0 <= index < len(items)):
            raise NotFoundError("Item")
        return items[index]

    def update(self, items: List[T], index: int, detail: Detail, status: Status | None) -> None:
        """Update item at index."""
        item = self.get(items, index)
        self._validate(detail)
        self._update(item, detail, status)

    def delete(self, items: List[T], index: int) -> None:
        """Delete item at index."""
        item = self.get(items, index)
        items.remove(item)

    @abstractmethod
    def _validate(self, detail: Detail) -> None:
        """Validate detail."""
        raise NotImplementedError

    @abstractmethod
    def _create(self, items: List[T], detail: Detail) -> T:
        """Return new instance."""
        raise NotImplementedError

    @abstractmethod
    def _update(self, item: T, detail: Detail, status: Status | None) -> None:
        """Update an instance."""
        raise NotImplementedError
