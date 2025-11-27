from abc import ABC, abstractmethod
from datetime import date
from typing import TypeVar, Generic, List, Optional
from core.config import AppConfig
from core.validator import NonEmptyTextValidator, MaxCountValidator
from models.models import Detail, Project

T = TypeVar("T")


class BaseManager(ABC, Generic[T]):
    """Abstract base manager providing reusable CRUD operations with validator integration."""

    def __init__(self, config: AppConfig) -> None:
        self._config: AppConfig = config
        self._entity_list: List[T] = []

    def add_entity(self, detail: Detail, deadline: Optional[date] = None, status: Optional[str] = None) -> None:
        """Validate creation and append entity; all exceptions come from validators."""
        self.validate_creation()
        entity = self._create_entity_object(detail, deadline, status)
        self._entity_list.append(entity)

    def remove_entity_object(self, entity: T) -> None:
        """Remove entity; cascade delete for projects."""
        if isinstance(entity, Project):
            self._cascade_delete_tasks(entity)
        if entity in self._entity_list:
            self._entity_list.remove(entity)

    def get_entities(self) -> List[T]:
        return self._entity_list

    def update_entity_fields(
        self,
        entity: T,
        detail: Detail,
        deadline: Optional[date] = None,
        status: Optional[str] = None
    ) -> None:
        """Update entity fields with validators; skip_current_title used for editing."""
        self._update_entity_detail(entity, detail)
        self._update_deadline_and_status(deadline, entity, status)

    @abstractmethod
    def _update_deadline_and_status(self, deadline, entity, status):
        raise NotImplementedError

    @abstractmethod
    def entity_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def _create_entity_object(self, detail: Detail,
                              deadline: Optional[date] = None, status: Optional[str] = None) -> T:
        raise NotImplementedError

    @abstractmethod
    def _cascade_delete_tasks(self, entity) -> None:
        raise NotImplementedError

    @abstractmethod
    def _get_max_desc_length(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def _get_max_count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def _get_max_title_length(self) -> int:
        raise NotImplementedError

    def _update_entity_detail(self, entity: T, detail: Detail) -> None:
        entity.detail = detail

    # ---------- Validators ----------

    def validate_creation(self) -> None:
        """Validate entity creation using MaxCountValidator."""
        MaxCountValidator(
            max_count=self._get_max_count(),
            current_count=len(self._entity_list),
            field_name=self.entity_name()
        ).validate()

    def validate_title(self, title: str, skip_current: Optional[str] = None) -> None:
        """Validate title using NonEmptyTextValidator; skip_current used for editing."""
        NonEmptyTextValidator(
            max_length=self._get_max_title_length(),
            field_name=f"{self.entity_name()} title",
            existing_values=[e.detail.title for e in self._entity_list],
            skip_current=skip_current
        ).validate(title)

    def validate_description(self, description: str) -> None:
        """Validate description using NonEmptyTextValidator."""
        NonEmptyTextValidator(
            max_length=self._get_max_desc_length(),
            field_name=f"{self.entity_name()} description"
        ).validate(description)
