from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from app.models.models import Detail
from app.cli.base_menu import BaseMenu
from app.services.entity_service import EntityManager
from app.exceptions.entity import NotFoundError, ValidationError, LimitExceededError

T = TypeVar("T")


class EntityMenu(BaseMenu, ABC, Generic[T]):
    """Abstract base menu for managing entities."""

    def __init__(self, title: str, parent_menu: BaseMenu, entity_manager: EntityManager[T]) -> None:
        """Initialize the entity menu.

        Args:
            title (str): Menu title.
            parent_menu (BaseMenu): Parent menu for navigation.
            entity_manager (EntityManager[T]): Manager handling entity operations.
        """
        super().__init__(title, parent_menu)
        self._entity_manager: EntityManager[T] = entity_manager
        self._setup_options()

    @abstractmethod
    def _setup_options(self) -> None:
        """Register menu options."""
        raise NotImplementedError

    @abstractmethod
    def _get_extra_info(self, entity: T) -> str:
        """Return entity-specific info."""
        raise NotImplementedError

    @staticmethod
    def _get_input_detail() -> Detail:
        """Collect user input for detail."""
        title = input("Enter title: ").strip()
        description = input("Enter description: ").strip()
        return Detail(title=title, description=description)

    def _view_entities(self, entities: List[T], entity_name: str) -> None:
        """Render a list of entities or raise NotFoundError if empty.

        Args:
            entities (List[T]): List of entities.
            entity_name (str): Name of entity type.

        Raises:
            NotFoundError: If list is empty.
        """
        if not entities:
            raise NotFoundError(entity_name)
        for index, entity in enumerate(entities, start=1):
            title = getattr(entity.detail, "title", "Untitled")
            description = getattr(entity.detail, "description", "No description")
            extra = self._get_extra_info(entity)
            print(f"{index}. {title} {extra}- {description}")

    def _create_entity(self, parent: Optional[object], entity_name: str) -> None:
        """Create a new entity using the associated EntityManager.

        Args:
            parent (Optional[object]): Parent context (e.g., project for tasks).
            entity_name (str): Name of the entity.
        """
        try:
            detail = self._get_input_detail()
            self._entity_manager.create_entity(parent, detail)
            print(f"✅ {entity_name} created successfully.")
        except (ValidationError, LimitExceededError) as error:
            self._handle_error(error)

    def _update_entity_by_index(self, parent: object, entity_name: str, status: str = "") -> None:
        """Update an entity by selecting its index.

        Args:
            parent (object): Parent context (e.g., project or None).
            entity_name (str): Name of the entity to update.
            status (str): Task status if applicable.

        Raises:
            NotFoundError: If index invalid.
            ValidationError: If validation fails.
        """
        try:
            detail, index, status = self._get_updated_input(entity_name, parent, status)
            self._entity_manager.update_entity_by_index(parent, index, detail, status)
            print(f"✅ {entity_name} updated successfully.")
        except (NotFoundError, ValidationError, ValueError) as error:
            self._handle_error(error)

    def _get_updated_input(self, entity_name, parent, status):
        collection = self._entity_manager.get_collection(parent)
        self._view_entities(collection, entity_name)
        index = int(input(f"Enter {entity_name.lower()} number: ")) - 1
        detail = self._get_input_detail()
        if entity_name.lower() == "task":
            status = input("Enter status ('todo', 'doing', 'done'): ").strip()
        return detail, index, status

    def _delete_entity_by_index(self, parent: object, entity_name: str) -> None:
        """Delete an entity by selecting its index.

        Args:
            parent (object): Parent context (e.g., project or None).
            entity_name (str): Name of the entity to delete.
        """
        try:
            collection = self._entity_manager.get_collection(parent)
            self._view_entities(collection, entity_name)
            index = int(input(f"Enter {entity_name.lower()} number: ")) - 1
            self._entity_manager.remove_entity_by_index(parent, index)
            print(f"🗑️ {entity_name} deleted successfully.")
        except (NotFoundError, ValueError) as error:
            self._handle_error(error)

    def _handle_error(self, error: Exception) -> None:
        """Display formatted error.

        Args:
            error (Exception): Exception to handle.
        """
        if hasattr(error, "message") and callable(getattr(error, "message")):
            print(f"❌ {error.message()}")
        else:
            print(f"❌ {error}")
