from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List
from app.models.models import Detail, Status
from app.services.base_service import BaseManager
from app.exceptions.entity import AlreadyExistsError, LimitExceededError, NotFoundError, ValidationError

T = TypeVar("T")


class EntityManager(BaseManager[T], ABC, Generic[T]):
    """Manager for entity-specific CRUD operations."""

    def __init__(self, config) -> None:
        """Initialize internal entity list."""
        super().__init__(config)
        self._items: List[T] = []

    def create_entity(self, entity: T, detail: Detail) -> T:
        """Create entity with validation, uniqueness, and limit.

        Args:
            entity (T): Entity object to add.
            detail (Detail): Detail information.

        Returns:
            T: Created entity.

        Raises:
            AlreadyExistsError: If duplicate exists.
            LimitExceededError: If collection is full.
            ValidationError: If validation fails.
        """
        try:
            self._validate_detail(detail, *self._get_limits())
        except Exception as error:
            raise ValidationError(type(entity).__name__) from error

        if any(e.detail.title == detail.title for e in self._items):
            raise AlreadyExistsError(type(entity).__name__)

        if len(self._items) >= self._get_limit_count():
            raise LimitExceededError(type(entity).__name__)

        entity.detail = detail
        self._items.append(entity)
        return entity

    def update_entity(self, index: int, detail: Detail, status: Status | None = None) -> T:
        """Update entity at index.

        Args:
            index (int): Index of entity.
            detail (Detail): Updated detail.
            status (Status | None): Optional status (for tasks).

        Returns:
            T: Updated entity.

        Raises:
            NotFoundError: If index invalid.
            ValidationError: If validation fails.
        """
        if index < 0 or index >= len(self._items):
            raise NotFoundError("Entity")

        try:
            self._validate_detail(detail, *self._get_limits())
        except Exception as error:
            raise ValidationError(type(self._items[index]).__name__) from error

        entity = self._items[index]
        entity.detail = detail

        if status is not None:
            entity.status = status

        return entity

    def remove_entity(self, index: int) -> None:
        """Remove entity by index.

        Args:
            index (int): Index to remove.

        Raises:
            NotFoundError: If index invalid.
        """
        if index < 0 or index >= len(self._items):
            raise NotFoundError("Entity")
        del self._items[index]

    def list_entities(self) -> List[T]:
        """Return all entities.

        Returns:
            List[T]: All entities.
        """
        return list(self._items)

    @abstractmethod
    def _get_limit_count(self) -> int:
        """Return max number of allowed entities."""
        raise NotImplementedError

    @abstractmethod
    def _get_limits(self) -> tuple[int, int]:
        """Return max title and description length."""
        raise NotImplementedError
