from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional
from datetime import date
from models.models import Detail
from core.config import AppConfig

T = TypeVar("T")


class BaseManager(ABC, Generic[T]):
    """Abstract base manager providing reusable CRUD and validation template."""

    def __init__(self, config: AppConfig) -> None:
        self._config: AppConfig = config
        self._entity_list: List[T] = []

    def add_entity(self, detail: Detail, deadline: Optional[date] = None) -> None:
        """Validate, create, and append entity to entity_list."""
        self.assert_can_create()
        self.validate(detail)
        entity = self._create_entity_object(detail, deadline)
        self._entity_list.append(entity)

    def remove_entity_object(self, entity: T) -> None:
        """Remove entity from list by object reference."""
        try:
            self._entity_list.remove(entity)
        except ValueError:
            raise ValueError(f"{self._entity_name()} not found in entity list.")

    def get_entities(self) -> list[T]:
        return self._entity_list

    def _validate_entity_index(self, idx: int) -> None:
        if not (0 <= idx < len(self._entity_list)):
            raise IndexError("Invalid index.")

    def validate_title(self, title: str) -> None:
        max_title_len = getattr(self._config, f"max_{self._entity_name().lower()}_name_length")
        title = title.strip()
        if not title:
            raise ValueError(f"{self._entity_name()} title cannot be empty.")
        if len(title) > max_title_len:
            raise ValueError(f"{self._entity_name()} title cannot exceed {max_title_len} characters.")

    def validate_description(self, description: str) -> None:
        max_desc_len = getattr(self._config, f"max_{self._entity_name().lower()}_description_length")
        description = description.strip()
        if not description:
            raise ValueError(f"{self._entity_name()} description cannot be empty.")
        if len(description) > max_desc_len:
            raise ValueError(f"{self._entity_name()} description cannot exceed {max_desc_len} characters.")

    @abstractmethod
    def _entity_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def assert_can_create(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _create_entity_object(self, detail: Detail, deadline: Optional[date] = None) -> T:
        raise NotImplementedError

    @abstractmethod
    def _get_max_desc_length(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def _get_max_title_length(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def validate(self, detail: Detail) -> None:
        raise NotImplementedError

    def _update_entity_detail(self, entity: T, detail: Detail) -> None:
        entity.detail = detail

    def _assert_can_append(self, max_count: int):
        if len(self._entity_list) >= max_count:
            raise OverflowError(f"Maximum {self._entity_name()} count reached.")
