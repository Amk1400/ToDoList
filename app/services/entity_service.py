from abc import ABC
from typing import List, Generic, TypeVar
from app.models.models import Detail
from app.services.base_service import BaseManager
from app.exceptions.entity import AlreadyExistsError, LimitExceededError, ValidationError, NotFoundError

T = TypeVar("T")


class EntityManager(BaseManager[T], ABC, Generic[T]):
    """Abstract entity manager implementing shared logic."""

    def create_entity(self, parent, detail: Detail) -> None:
        """Create entity under parent if applicable.

        Args:
            parent: Parent container if needed.
            detail (Detail): Entity detail.

        Raises:
            AlreadyExistsError: If title exists.
            LimitExceededError: If limit exceeded.
            ValidationError: If validation fails.
        """
        collection = self.get_collection(parent)
        if any(e.detail.title == detail.title for e in collection):
            raise AlreadyExistsError(self._entity_type().__name__)
        if len(collection) >= self._get_limit(parent):
            raise LimitExceededError(self._entity_type().__name__)
        try:
            self.create(collection, detail, self._get_limit(parent))
        except ValidationError as error:
            raise ValidationError(self._entity_type().__name__) from error

    def get_entity_by_index(self, parent, index: int) -> T:
        """Retrieve entity by index.

        Args:
            parent: Parent container if applicable.
            index (int): Entity index.

        Returns:
            T: Entity instance.

        Raises:
            NotFoundError: If invalid index.
        """
        collection = self.get_collection(parent)
        try:
            return self.get_entity(collection, index)
        except NotFoundError as error:
            raise NotFoundError(self._entity_type().__name__) from error

    def remove_entity_by_index(self, parent, index: int) -> None:
        """Remove entity by index.

        Args:
            parent: Parent container if applicable.
            index (int): Entity index.

        Raises:
            NotFoundError: If invalid index.
        """
        collection = self.get_collection(parent)
        try:
            self.remove_entity(collection, index)
        except NotFoundError as error:
            raise NotFoundError(self._entity_type().__name__) from error

    def update_entity_by_index(self, parent, index: int, detail: Detail, status: str) -> None:
        """Update entity detail.

        Args:
            parent: Parent container.
            index (int): Entity index.
            detail (Detail): New detail.
            status (str): task status

        Raises:
            NotFoundError: If not found.
            ValidationError: If invalid.
        """
        collection = self.get_collection(parent)
        try:
            self.update_entity(collection, index, detail, status)
        except (NotFoundError, ValidationError) as error:
            raise type(error)(self._entity_type().__name__) from error

    @staticmethod
    def _get_limit(parent) -> int:
        """Return entity limit."""
        raise NotImplementedError

    @staticmethod
    def get_collection(parent) -> List[T]:
        """Return entity collection."""
        raise NotImplementedError