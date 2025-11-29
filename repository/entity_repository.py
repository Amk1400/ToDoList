from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List
from db.db_inmemory import InMemoryDatabase

T = TypeVar("T")


class EntityRepository(ABC, Generic[T]):
    """Abstract repository for generic entity operations."""

    def __init__(self, db: InMemoryDatabase) -> None:
        self._db: InMemoryDatabase = db

    @abstractmethod
    def get_db_list(self, project: object | None = None) -> List[T]:
        """Return list of entities; project is required for nested entities like Task."""
        raise NotImplementedError

    @abstractmethod
    def append_to_db(self, entity: T, project: object | None = None) -> None:
        """Add entity to database; project is required for nested entities like Task."""
        raise NotImplementedError

    @abstractmethod
    def remove_from_db(self, entity: T, project: object | None = None) -> None:
        """Remove entity from database; project is required for nested entities like Task."""
        raise NotImplementedError
