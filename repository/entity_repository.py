from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List
from db.db import DataBase

T = TypeVar("T")


class EntityRepository(ABC, Generic[T]):
    """Abstract repository for generic entity operations."""

    def __init__(self, db: DataBase) -> None:
        self._db: DataBase = db

    @abstractmethod
    def get_db_list(self, *args, **kwargs) -> List[T]:
        """Return list of entities."""
        raise NotImplementedError

    @abstractmethod
    def append_to_db(self, *args, **kwargs) -> None:
        """Add entity to database."""
        raise NotImplementedError

    @abstractmethod
    def remove_from_db(self, *args, **kwargs) -> None:
        """Remove entity from database."""
        raise NotImplementedError
