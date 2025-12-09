from abc import ABC, abstractmethod
from datetime import date
from typing import TypeVar, Generic, List, Optional

from core.config import AppConfig
from models.models import Detail, Project
from repository.entity_repository import EntityRepository
from service.validators import Validators

T = TypeVar("T")


class EntityManager(ABC, Generic[T]):
    """Abstract base manager for entity CRUD operations."""
    """
    Attributes:
        _config (AppConfig): Application configuration.
        _repository (EntityRepository[T]): Storage repository.
    """

    def __init__(self, config: AppConfig, repository: EntityRepository[T]) -> None:
        """Initialize entity manager with config and repository."""
        """
        Args:
            config (AppConfig): App configuration.
            repository (EntityRepository[T]): Repository instance.

        Returns:
            None: No return value.

        Raises:
            None
        """
        self._config: AppConfig = config
        self._repository: EntityRepository[T] = repository

    def add_entity(
        self,
        detail: Detail,
        deadline: Optional[date] = None,
        status: Optional[str] = None,
    ) -> None:
        """Validate and add new entity."""
        """
        Args:
            detail (Detail): Metadata for entity.
            deadline (Optional[date]): Deadline value.
            status (Optional[str]): Status for entity.

        Returns:
            None: No return value.

        Raises:
            ValueError: If validation fails.
        """
        Validators.validate_creation(
            self.entity_name(),
            len(self.get_repo_list()),
            self._get_max_count(),
        )
        entity = self.create_entity_object(detail, deadline, status)
        self._append_to_repository(entity)

    @abstractmethod
    def remove_entity_object(self, entity: T) -> None:
        """Remove entity wrapper."""
        """
        Args:
            entity (T): Target entity.

        Returns:
            None

        Raises:
            NotImplementedError: If subclass does not implement.
        """
        raise NotImplementedError

    @abstractmethod
    def get_repo_list(self) -> List[T]:
        """Return repository items."""
        """
        Args:
            None

        Returns:
            List[T]: Entity list.

        Raises:
            NotImplementedError: If subclass does not implement.
        """
        raise NotImplementedError

    def update_entity_object(
        self,
        old_entity: T,
        new_entity: T,
        parent_project: Optional[Project] = None,
    ) -> None:
        """Update stored entity."""
        """
        Args:
            old_entity (T): Original instance.
            new_entity (T): Updated instance.
            parent_project (Optional[Project]): Parent project.

        Returns:
            None

        Raises:
            Exception: If repository update fails.
        """
        self._repository.update_entity(parent_project, old_entity, new_entity)

    def _append_to_repository(self, entity: T) -> None:
        """Append entity to repository."""
        """
        Args:
            entity (T): Entity to append.

        Returns:
            None

        Raises:
            None
        """
        self._repository.append_to_db(entity)  # type: ignore

    @abstractmethod
    def _remove_from_repository(
        self,
        entity: T,
        parent_project: Optional[Project] = None,
    ) -> None:
        """Remove entity from repository."""
        """
        Args:
            entity (T): Target entity.
            parent_project (Optional[Project]): Optional project.

        Returns:
            None

        Raises:
            NotImplementedError: If subclass does not implement.
        """
        raise NotImplementedError

    @staticmethod
    def _update_detail_by_repo(entity: T, detail: Detail) -> None:
        """Update entity detail reference."""
        """
        Args:
            entity (T): Entity object.
            detail (Detail): New detail.

        Returns:
            None

        Raises:
            None
        """
        entity.detail = detail

    @abstractmethod
    def _update_deadline_and_status_by_repo(self, deadline, entity, status):
        """Update deadline and status."""
        """
        Args:
            deadline: Optional deadline.
            entity: Entity instance.
            status: Optional status.

        Returns:
            None

        Raises:
            NotImplementedError: If subclass does not implement.
        """
        raise NotImplementedError

    @abstractmethod
    def entity_name(self) -> str:
        """Return name of entity type."""
        """
        Args:
            None

        Returns:
            str: Entity type name.

        Raises:
            NotImplementedError: If subclass does not implement.
        """
        raise NotImplementedError

    @abstractmethod
    def create_entity_object(
        self,
        detail: Detail,
        deadline: Optional[date] = None,
        status: Optional[str] = None,
    ) -> T:
        """Create entity instance."""
        """
        Args:
            detail (Detail): Entity details.
            deadline (Optional[date]): Deadline value.
            status (Optional[str]): Status value.

        Returns:
            T: Created entity.

        Raises:
            NotImplementedError: If subclass does not implement.
        """
        raise NotImplementedError

    @abstractmethod
    def _get_max_desc_length(self) -> int:
        """Get maximum description length."""
        """
        Args:
            None

        Returns:
            int: Maximum description length.

        Raises:
            NotImplementedError: If subclass does not implement.
        """
        raise NotImplementedError

    @abstractmethod
    def _get_max_count(self) -> int:
        """Get maximum number of entities."""
        """
        Args:
            None

        Returns:
            int: Max count.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    @abstractmethod
    def _get_max_title_length(self) -> int:
        """Get max title length."""
        """
        Args:
            None

        Returns:
            int: Maximum allowed title length.

        Raises:
            NotImplementedError: If subclass does not implement.
        """
        raise NotImplementedError
