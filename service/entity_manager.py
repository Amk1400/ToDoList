from abc import ABC, abstractmethod
from datetime import date
from typing import TypeVar, Generic, List, Optional
from core.config import AppConfig
from models.models import Detail, Project
from repository.entity_repository import EntityRepository
from core.validator import NonEmptyTextValidator, MaxCountValidator

T = TypeVar("T")


class EntityManager(ABC, Generic[T]):
    """Base manager providing CRUD operations with validator integration."""

    def __init__(self, config: AppConfig, repository: EntityRepository[T]) -> None:
        self._config: AppConfig = config
        self._repository: EntityRepository[T] = repository

    def add_entity(self, detail: Detail, deadline: Optional[date] = None, status: Optional[str] = None) -> None:
        """Validate and add entity."""
        self.validate_creation()
        entity = self.create_entity_object(detail, deadline, status)
        self._append_to_repository(entity)

    @abstractmethod
    def remove_entity_object(self, entity: T) -> None:
        """Remove entity and handle cascade deletes if needed."""
        raise NotImplementedError

    @abstractmethod
    def get_repo_list(self) -> List[T]:
        raise NotImplementedError

    def update_entity_object(self, old_entity: T, new_entity: T, parent_project: Optional[Project] = None) -> None:
        """Update an entity in repository."""
        self._repository.update_entity(parent_project, old_entity, new_entity)

    def _append_to_repository(self, entity: T) -> None:
        """Append entity to repository."""
        self._repository.append_to_db(entity)  # type: ignore

    @abstractmethod
    def _remove_from_repository(self, entity: T, parent_project: Optional[Project] = None) -> None:
        raise NotImplementedError

    @staticmethod
    def _update_detail_by_repo(entity: T, detail: Detail) -> None:
        entity.detail = detail

    @abstractmethod
    def _update_deadline_and_status_by_repo(self, deadline, entity, status):
        raise NotImplementedError

    @abstractmethod
    def entity_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def create_entity_object(
        self, detail: Detail, deadline: Optional[date] = None, status: Optional[str] = None
    ) -> T:
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

    # ---------- Validators ----------

    def validate_creation(self) -> None:
        """Validate max count."""
        MaxCountValidator(
            max_count=self._get_max_count(),
            current_count=len(self.get_repo_list()),
            field_name=self.entity_name()
        ).validate()

    def validate_title(self, title: str, skip_current: Optional[str] = None) -> None:
        """Validate title for non-empty and max length."""
        NonEmptyTextValidator(
            max_length=self._get_max_title_length(),
            field_name=f"{self.entity_name()} title",
            existing_values=[e.detail.title for e in self.get_repo_list()],
            skip_current=skip_current
        ).validate(title)

    def validate_description(self, description: str) -> None:
        """Validate description for non-empty and max length."""
        NonEmptyTextValidator(
            max_length=self._get_max_desc_length(),
            field_name=f"{self.entity_name()} description"
        ).validate(description)
