from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic
from models import Detail
from config import AppConfig

T = TypeVar("T")


class BaseManager(ABC, Generic[T]):
    """Abstract base manager providing reusable CRUD and validation template."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize base manager with configuration."""
        self._config: AppConfig = config

    def create(self, items: List[T], detail: Detail, max_count: int) -> None:
        """Template method for creating an entity."""
        if len(items) >= max_count:
            raise OverflowError(f"Maximum number of {self._entity_name()}s reached.")
        self._validate(detail)
        items.append(self._create_entity(detail))

    def get_entity(self, items: List[T], index: int) -> T:
        """Retrieve an entity by index."""
        if not (0 <= index < len(items)):
            raise IndexError(f"Invalid {self._entity_name().lower()} index.")
        return items[index]

    def remove_entity(self, items: List[T], index: int) -> None:
        """Remove an entity by index."""
        entity = self.get_entity(items, index)
        items.remove(entity)

    def update_entity(self, items: List[T], index: int, detail: Detail) -> None:
        """Update entity details."""
        entity = self.get_entity(items, index)
        self._validate(detail)
        self._update_entity_detail(entity, detail)

    @abstractmethod
    def _entity_name(self) -> str:
        """Return entity name (for error messages)."""
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

    def _validate_detail(
        self,
        detail: Detail,
        max_title_len: int,
        max_desc_len: int,
        entity_name: str
    ) -> None:
        """Generic validator for Detail objects."""
        title, description = detail.title.strip(), detail.description.strip()

        if not title:
            raise ValueError(f"{entity_name} title cannot be empty.")
        if len(title) > max_title_len:
            raise ValueError(f"{entity_name} title cannot exceed {max_title_len} characters.")
        if not description:
            raise ValueError(f"{entity_name} description cannot be empty.")
        if len(description) > max_desc_len:
            raise ValueError(f"{entity_name} description cannot exceed {max_desc_len} characters.")
