from abc import abstractmethod
from typing import TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session

T = TypeVar("T")


class EntityPostgres(Generic[T]):
    """Base class for Postgres entities."""

    @abstractmethod
    def add_entity(self, entity: T, container: List[T], session: Session, parent: Optional[T] = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_entity(self, entity: T, container: List[T], session: Session, parent: Optional[T] = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_entity(self, old_entity: T, new_entity: T, container: List[T], session: Session, parent: Optional[T] = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def load_all(self, session: Session) -> List[T]:
        raise NotImplementedError