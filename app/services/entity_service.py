from abc import ABC, abstractmethod
from typing import List, Generic, TypeVar
from app.models.models import Detail, Status
from app.services.base_service import BaseManager
from app.exceptions.entity import AlreadyExistsError, LimitExceededError
T = TypeVar("T")


class EntityManager(BaseManager[T], ABC, Generic[T]):
    """Manager for entity-specific operations (uniqueness, limit, collection)."""

    def create_entity(self, parent, detail: Detail) -> None:
        """Create entity in parent collection, enforcing uniqueness and limit."""
        collection = self.get_collection(parent)
        if any(e.detail.title == detail.title for e in collection):
            raise AlreadyExistsError("Entity")
        if len(collection) >= self._get_limit(parent):
            raise LimitExceededError("Entity")
        self.create(collection, detail)

    def get_entity_by_index(self, parent, index: int) -> T:
        return self.get(self.get_collection(parent), index)

    def update_entity_by_index(self, parent, index: int, detail: Detail, status: Status | None) -> None:
        self.update(self.get_collection(parent), index, detail, status)

    def remove_entity_by_index(self, parent, index: int) -> None:
        self.delete(self.get_collection(parent), index)

    @staticmethod
    @abstractmethod
    def _get_limit(parent) -> int:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_collection(parent) -> List[T]:
        raise NotImplementedError
