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
        entity = self._create_entity_object(detail, deadline)
        self._entity_list.append(entity)

    def remove_entity_object(self, entity: T) -> None:
        """Remove entity from list by object reference."""
        try:
            self._entity_list.remove(entity)
        except ValueError:
            raise ValueError(f"{self.entity_name()} not found in entity list.")

    def get_entities(self) -> list[T]:
        return self._entity_list

    def update_entity_fields(
        self,
        entity: T,
        detail: Detail,
        deadline: Optional[date] = None,
        status: Optional[str] = None
    ) -> None:
        """Update mandatory detail and optional fields on entity."""
        self._update_entity_detail(entity, detail)
        self._update_deadline_and_status(deadline, entity, status)

    @abstractmethod
    def _update_deadline_and_status(self, deadline, entity, status):
        raise NotImplementedError

    @abstractmethod
    def entity_name(self) -> str:
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

    def _update_entity_detail(self, entity: T, detail: Detail) -> None:
        entity.detail = detail

    def _assert_can_append(self, max_count: int):
        if len(self._entity_list) >= max_count:
            raise OverflowError(f"Maximum {self.entity_name()} count reached.")

    def validate_title(self, title: str) -> None:
        """Validate title: non-empty, within length, and unique."""
        self._validate_detail(self._get_max_title_length(), title, "title")
        self._check_title_unique(title)

    def _check_title_unique(self, title):
        if any(entity.detail.title == title for entity in self._entity_list):
            raise ValueError(f"{self.entity_name()} title must be unique.")

    def validate_description(self, description: str) -> None:
        self._validate_detail(self._get_max_desc_length(), description, "description")

    def _validate_detail(self, max_length:int, detail:str, detail_name: str):
        if not detail:
            raise ValueError(f"{self.entity_name()} {detail_name} cannot be empty.")
        if len(detail) > max_length:
            raise ValueError(f"{self.entity_name()} {detail_name} cannot exceed {max_length} characters.")
