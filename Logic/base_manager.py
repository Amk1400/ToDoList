from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic
from models import Detail
from config import AppConfig

T = TypeVar("T")


class BaseManager(ABC, Generic[T]):
    """Abstract base manager providing reusable CRUD and validation logic."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize base manager with configuration.

        Args:
            config (AppConfig): Configuration object containing validation limits.
        """
        self._config: AppConfig = config

    def create(self, items: List[T], detail: Detail, max_count: int) -> None:
        """Create a new entity after validation.

        Args:
            items (List[T]): The list to which the new entity will be added.
            detail (Detail): The detail data used to create the entity.
            max_count (int): Maximum allowed entities.

        Raises:
            OverflowError: If the maximum count of entities is reached.
            ValueError: If the provided detail fails validation.
        """
        if len(items) >= max_count:
            raise OverflowError(f"Maximum number of {self._entity_name()}s reached.")
        self._validate(detail)
        items.append(self._create_entity(detail))

    def get_entity(self, items: List[T], index: int) -> T:
        """Retrieve an entity by index.

        Args:
            items (List[T]): The list of entities.
            index (int): The index of the entity to retrieve.

        Returns:
            T: The entity at the specified index.

        Raises:
            IndexError: If the index is out of range.
        """
        if not (0 <= index < len(items)):
            raise IndexError(f"Invalid {self._entity_name().lower()} index.")
        return items[index]

    def remove_entity(self, items: List[T], index: int) -> None:
        """Remove an entity by index.

        Args:
            items (List[T]): The list of entities.
            index (int): The index of the entity to remove.

        Raises:
            IndexError: If the index is invalid.
        """
        entity = self.get_entity(items, index)
        items.remove(entity)

    def update_entity(self, items: List[T], index: int, detail: Detail) -> None:
        """Update an entity’s detail after validation.

        Args:
            items (List[T]): The list of entities.
            index (int): The index of the entity to update.
            detail (Detail): The new detail values.

        Raises:
            IndexError: If the index is invalid.
            ValueError: If validation fails.
        """
        entity = self.get_entity(items, index)
        self._validate(detail)
        self._update_entity_detail(entity, detail)

    @abstractmethod
    def _entity_name(self) -> str:
        """Return the entity name for error messages.

        Returns:
            str: The name of the managed entity.
        """
        raise NotImplementedError

    @abstractmethod
    def _create_entity(self, detail: Detail) -> T:
        """Factory method for creating an entity instance.

        Args:
            detail (Detail): Detail data for entity creation.

        Returns:
            T: A new entity instance.
        """
        raise NotImplementedError

    @abstractmethod
    def _validate(self, detail: Detail) -> None:
        """Validate an entity’s detail data.

        Args:
            detail (Detail): The detail data to validate.

        Raises:
            ValueError: If validation fails.
        """
        raise NotImplementedError

    @abstractmethod
    def _update_entity_detail(self, entity: T, detail: Detail) -> None:
        """Apply updated details to an existing entity.

        Args:
            entity (T): The entity to update.
            detail (Detail): The new detail data.
        """
        raise NotImplementedError

    def _validate_detail(
        self,
        detail: Detail,
        max_title_len: int,
        max_desc_len: int,
        entity_name: str
    ) -> None:
        """Validate common title and description constraints for Detail objects.

        Args:
            detail (Detail): The detail object containing title and description.
            max_title_len (int): Maximum allowed length for the title.
            max_desc_len (int): Maximum allowed length for the description.
            entity_name (str): The name of the entity being validated.

        Raises:
            ValueError: If title or description is empty or exceeds the limits.
        """
        title, description = detail.title.strip(), detail.description.strip()

        if not title:
            raise ValueError(f"{entity_name} title cannot be empty.")
        if len(title) > max_title_len:
            raise ValueError(f"{entity_name} title cannot exceed {max_title_len} characters.")
        if not description:
            raise ValueError(f"{entity_name} description cannot be empty.")
        if len(description) > max_desc_len:
            raise ValueError(f"{entity_name} description cannot exceed {max_desc_len} characters.")
