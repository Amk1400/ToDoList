from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

from db.db_interface import DatabaseInterface
from models.models import Project

T = TypeVar("T")


class EntityRepository(ABC, Generic[T]):
    """Abstract repository for basic entity operations."""

    def __init__(self, db: DatabaseInterface[T]) -> None:
        """Initialize repository with a database dependency.

        Args:
            db (DatabaseInterface[T]): Database layer used for entity persistence.
        """
        self._db: DatabaseInterface[T] = db

    @abstractmethod
    def get_db_list(self, project: object | None = None) -> List[T]:
        """Return list of stored entities.

        Args:
            project (object | None): Parent project for nested structures.

        Returns:
            List[T]: Collection of stored entities.

        Raises:
            NotImplementedError: Method not implemented in subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def append_to_db(self, entity: T, project: object | None = None) -> None:
        """Insert a new entity into storage.

        Args:
            entity (T): Entity instance to be added.
            project (object | None): Parent project for nested structures.

        Returns:
            None: No return value.

        Raises:
            NotImplementedError: Method not implemented in subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def remove_from_db(self, entity: T, project: object | None = None) -> None:
        """Delete an entity from storage.

        Args:
            entity (T): Entity instance to be removed.
            project (object | None): Parent project for nested structures.

        Returns:
            None: No return value.

        Raises:
            NotImplementedError: Method not implemented in subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def update_entity(
        self,
        parent_project: Project | None,
        old_entity: T,
        new_entity: T
    ) -> None:
        """Update an existing stored entity.

        Args:
            parent_project (Project | None): Parent project for nested entities.
            old_entity (T): Current entity instance being replaced.
            new_entity (T): Updated entity instance.

        Returns:
            None: No return value.

        Raises:
            NotImplementedError: Method not implemented in subclass.
        """
        raise NotImplementedError
