from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List
from datetime import date
from models.models import Detail
from core.config import AppConfig

T = TypeVar("T")


class BaseManager(ABC, Generic[T]):
    """Abstract base manager providing reusable CRUD and validation template."""

    def __init__(self, config: AppConfig) -> None:
        self._config: AppConfig = config

    def _validate_title(self, title: str) -> None:
        max_title_len = getattr(self._config, f"max_{self._entity_name().lower()}_name_length")
        title = title.strip()
        if not title:
            raise ValueError(f"{self._entity_name()} title cannot be empty.")
        if len(title) > max_title_len:
            raise ValueError(f"{self._entity_name()} title cannot exceed {max_title_len} characters.")

    def _validate_description(self, description: str) -> None:
        max_desc_len = getattr(self._config, f"max_{self._entity_name().lower()}_description_length")
        description = description.strip()
        if not description:
            raise ValueError(f"{self._entity_name()} description cannot be empty.")
        if len(description) > max_desc_len:
            raise ValueError(f"{self._entity_name()} description cannot exceed {max_desc_len} characters.")

    def _validate_detail(self, detail: Detail, max_title_len: int, max_desc_len: int, entity_name: str) -> None:
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
        from datetime import date as today
        if deadline < today.today():
            raise ValueError("Deadline cannot be in the past.")

    @abstractmethod
    def _entity_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def assert_can_create(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _create_entity(self, detail: Detail) -> T:
        raise NotImplementedError

    @abstractmethod
    def _validate(self, detail: Detail) -> None:
        raise NotImplementedError

    @abstractmethod
    def _update_entity_detail(self, entity: T, detail: Detail) -> None:
        raise NotImplementedError
