from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List
from app.models.models import Detail
from app.core.config import AppConfig
from app.exceptions.entity import ValidationError, LimitExceededError, NotFoundError

T = TypeVar("T")


class BaseManager(ABC, Generic[T]):
    """Abstract base manager providing reusable CRUD and validation logic."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize base manager.

        Args:
            config (AppConfig): Application configuration.
        """
        self._config: AppConfig = config

    def create(self, items: List[T], detail: Detail, max_count: int) -> None:
        """Create a new entity after validation.

        Args:
            items (List[T]): Entity collection.
            detail (Detail): Data for new entity.
            max_count (int): Maximum allowed count.

        Raises:
            LimitExceededError: If max limit reached.
            ValidationError: If validation fails.
        """
        if len(items) >= max_count:
            raise LimitExceededError(self._entity_type().__name__)
        self._validate(detail)
        items.append(self._create_entity(detail))

    def get_entity(self, items: List[T], index: int) -> T:
        """Retrieve entity by index.

        Args:
            items (List[T]): Entity list.
            index (int): Index position.

        Returns:
            T: Entity instance.

        Raises:
            NotFoundError: If index invalid.
        """
        if not (0 <= index < len(items)):
            raise NotFoundError(self._entity_type().__name__)
        return items[index]

    def remove_entity(self, items: List[T], index: int) -> None:
        """Remove entity by index.

        Args:
            items (List[T]): Entity list.
            index (int): Index to remove.

        Raises:
            NotFoundError: If index invalid.
        """
        entity = self.get_entity(items, index)
        items.remove(entity)

    def update_entity(self, items: List[T], index: int, detail: Detail) -> None:
        """Update entity detail.

        Args:
            items (List[T]): Entity list.
            index (int): Index to update.
            detail (Detail): New detail.

        Raises:
            NotFoundError: If index invalid.
            ValidationError: If validation fails.
        """
        entity = self.get_entity(items, index)
        self._validate(detail)
        self._update_entity_detail(entity, detail)

    def _validate_detail(self, detail: Detail, max_title: int, max_desc: int) -> None:
        """Validate title and description length.

        Args:
            detail (Detail): Entity details.
            max_title (int): Max title length.
            max_desc (int): Max description length.

        Raises:
            ValidationError: If invalid data.
        """
        title, desc = detail.title.strip(), detail.description.strip()
        if not title or len(title) > max_title:
            raise ValidationError(self._entity_type().__name__)
        if not desc or len(desc) > max_desc:
            raise ValidationError(self._entity_type().__name__)

    @abstractmethod
    def _entity_type(self) -> type:
        """Return entity type."""
        raise NotImplementedError

    @abstractmethod
    def _create_entity(self, detail: Detail) -> T:
        """Create entity instance."""
        raise NotImplementedError

    @abstractmethod
    def _validate(self, detail: Detail) -> None:
        """Validate entity detail."""
        raise NotImplementedError

    @abstractmethod
    def _update_entity_detail(self, entity: T, detail: Detail) -> None:
        """Update entity detail."""
        raise NotImplementedError
