from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic
from app.models.models import Detail, Project, Task
from app.core.config import AppConfig
from app.exceptions.entity import ValidationError, LimitExceededError, NotFoundError

T = TypeVar("T")


class BaseManager(ABC, Generic[T]):
    """Abstract base manager providing reusable CRUD and validation logic.

    Attributes:
        _config (AppConfig): Configuration defining validation limits.
    """

    def __init__(self, config: AppConfig) -> None:
        """Initialize base manager.

        Args:
            config (AppConfig): Application configuration.
        """
        self._config: AppConfig = config

    def create(self, items: List[T], detail: Detail, max_count: int) -> None:
        """Create a new entity after validation.

        Args:
            items (List[T]): Collection of entities.
            detail (Detail): Data used to create the entity.
            max_count (int): Maximum number of allowed entities.

        Raises:
            LimitExceededError: If entity limit is exceeded.
            ValidationError: If entity validation fails.
        """
        if len(items) >= max_count:
            raise LimitExceededError(items[0] if items else Project(Detail("", "")))
        self._validate(detail)
        items.append(self._create_entity(detail))

    def get_entity(self, items: List[T], index: int) -> T:
        """Retrieve an entity by index.

        Args:
            items (List[T]): Collection of entities.
            index (int): Position of the entity to retrieve.

        Returns:
            T: The entity at the given index.

        Raises:
            NotFoundError: If the index is invalid.
        """
        if not (0 <= index < len(items)):
            raise NotFoundError(items[0] if items else Project(Detail("", "")))
        return items[index]

    def remove_entity(self, items: List[T], index: int) -> None:
        """Remove an entity by index.

        Args:
            items (List[T]): Collection of entities.
            index (int): Position of entity to remove.

        Raises:
            NotFoundError: If entity index is invalid.
        """
        entity = self.get_entity(items, index)
        items.remove(entity)

    def update_entity(self, items: List[T], index: int, detail: Detail) -> None:
        """Update an entity’s details after validation.

        Args:
            items (List[T]): Collection of entities.
            index (int): Index of entity to update.
            detail (Detail): New detail values.

        Raises:
            NotFoundError: If entity index is invalid.
            ValidationError: If validation fails.
        """
        entity = self.get_entity(items, index)
        self._validate(detail)
        self._update_entity_detail(entity, detail)

    @abstractmethod
    def _entity_name(self) -> str:
        """Return the entity name for display or logs.

        Returns:
            str: Entity name.
        """
        raise NotImplementedError

    @abstractmethod
    def _create_entity(self, detail: Detail) -> T:
        """Factory method to create a new entity instance.

        Args:
            detail (Detail): Data used to construct the entity.

        Returns:
            T: The new entity.
        """
        raise NotImplementedError

    @abstractmethod
    def _validate(self, detail: Detail) -> None:
        """Validate entity detail data.

        Args:
            detail (Detail): Data to validate.

        Raises:
            ValidationError: If validation fails.
        """
        raise NotImplementedError

    @abstractmethod
    def _update_entity_detail(self, entity: T, detail: Detail) -> None:
        """Apply updated details to an existing entity.

        Args:
            entity (T): Entity being updated.
            detail (Detail): New data to apply.
        """
        raise NotImplementedError

    def _validate_detail(
        self,
        detail: Detail,
        max_title_len: int,
        max_desc_len: int,
        entity_name: str,
    ) -> None:
        """Validate title and description constraints.

        Args:
            detail (Detail): Entity details.
            max_title_len (int): Maximum title length.
            max_desc_len (int): Maximum description length.
            entity_name (str): Entity name.

        Raises:
            ValidationError: If constraints are violated.
        """
        title, description = detail.title.strip(), detail.description.strip()

        if not title or len(title) > max_title_len:
            raise ValidationError(Project(detail))
        if not description or len(description) > max_desc_len:
            raise ValidationError(Project(detail))
