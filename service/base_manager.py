from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic
from datetime import date
from models import Detail
from core.config import AppConfig

T = TypeVar("T")


class BaseManager(ABC, Generic[T]):
    """Abstract base manager providing reusable CRUD and validation template."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize base manager with configuration.

        Args:
            config (AppConfig): Configuration limits.
        """
        self._config: AppConfig = config

    def create(self, items: List[T], detail: Detail, max_count: int) -> None:
        """Template method for creating an entity.

        Args:
            items (List[T]): Existing list of entities.
            detail (Detail): Entity detail.
            max_count (int): Max allowed count.

        Raises:
            OverflowError: When entity count exceeds max_count.
            ValueError: If detail validation fails.
        """
        if len(items) >= max_count:
            raise OverflowError(f"Maximum number of {self._entity_name()}s reached.")
        self._validate(detail)
        items.append(self._create_entity(detail))

    def get_entity(self, items: List[T], index: int) -> T:
        """Retrieve an entity by index.

        Args:
            items (List[T]): List of entities.
            index (int): Entity index.

        Returns:
            T: The requested entity.

        Raises:
            IndexError: If index is invalid.
        """
        if not (0 <= index < len(items)):
            raise IndexError(f"Invalid {self._entity_name().lower()} index.")
        return items[index]

    def remove_entity(self, items: List[T], index: int) -> None:
        """Remove an entity by index.

        Args:
            items (List[T]): List of entities.
            index (int): Entity index.

        Raises:
            IndexError: If index is invalid.
        """
        entity = self.get_entity(items, index)
        items.remove(entity)

    def update_entity(self, items: List[T], index: int, detail: Detail) -> None:
        """Update entity details.

        Args:
            items (List[T]): List of entities.
            index (int): Entity index.
            detail (Detail): Updated detail.

        Raises:
            IndexError: If entity index invalid.
            ValueError: If detail validation fails.
        """
        entity = self.get_entity(items, index)
        self._validate(detail)
        self._update_entity_detail(entity, detail)

    def _validate_detail(
        self,
        detail: Detail,
        max_title_len: int,
        max_desc_len: int,
        entity_name: str
    ) -> None:
        """Validate Detail object fields.

        Args:
            detail (Detail): Detail object.
            max_title_len (int): Max title length.
            max_desc_len (int): Max description length.
            entity_name (str): Entity name.

        Raises:
            ValueError: If title/description invalid.
        """
        title, description = detail.title.strip(), detail.description.strip()
        if not title:
            raise ValueError(f"{entity_name} title cannot be empty.")
        if len(title) > max_title_len:
            raise ValueError(f"{entity_name} title cannot exceed {max_title_len} characters.")
        if not description:
            raise ValueError(f"{entity_name} description cannot be empty.")
        if len(description) > max_desc_len:
            raise ValueError(f"{entity_name} description cannot exceed {max_desc_len} characters.")

    def _validate_deadline(self, deadline: date) -> None:
        """Validate deadline to ensure it's not in the past.

        Args:
            deadline (date): Task deadline.

        Raises:
            ValueError: If deadline is in the past.
        """
        from datetime import date as today
        if deadline < today.today():
            raise ValueError("Deadline cannot be in the past.")

    @abstractmethod
    def _entity_name(self) -> str:
        """Return entity name."""
        raise NotImplementedError

    @abstractmethod
    def _create_entity(self, detail: Detail) -> T:
        """Factory method for creating the entity."""
        raise NotImplementedError

    @abstractmethod
    def _validate(self, detail: Detail) -> None:
        """Validate detail fields."""
        raise NotImplementedError

    @abstractmethod
    def _update_entity_detail(self, entity: T, detail: Detail) -> None:
        """Apply updated details to an existing entity."""
        raise NotImplementedError
