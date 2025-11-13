from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Tuple
from app.models.models import Detail, Status
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

    @staticmethod
    def _get_input_detail() -> Detail:
        """Collect user input for detail."""
        title = input("Enter title: ").strip()
        description = input("Enter description: ").strip()
        return Detail(title=title, description=description)

    def _view_entities(self, entities: List[T], entity_name: str) -> None:
        """Render a list of entities or raise NotFoundError if empty."""
        if not entities:
            raise NotFoundError(entity_name)
        for index, entity in enumerate(entities, start=1):
            print(f"{index}. {entity}")

    def _get_entity_update_input(
            self, parent: object, entity_name: str
    ) -> Tuple[int, Detail, Optional[Status]]:
        """Collect entity index, updated details, and optional status.

        Args:
            parent (object): Parent context (project or None).
            entity_name (str): Name of entity (Task or Project).

        Returns:
            Tuple[int, Detail, Optional[Status]]: Index, detail, and optional status.
        """
        collection = self._entity_manager.get_collection(parent)
        self._view_entities(collection, entity_name)
        index = int(input(f"Enter {entity_name.lower()} number: ")) - 1
        detail = self._get_input_detail()
        status: Optional[Status] = None

        if entity_name == "Task":
            while True:
                raw_status = input("Enter preferred status (todo/doing/done): ").strip().lower()
                try:
                    status = Status(raw_status)
                    break
                except ValueError:
                    print("⚠ Invalid status. Please enter 'todo', 'doing', or 'done'.")

        return index, detail, status

    def _create_entity(self, parent: Optional[object], entity_name: str) -> None:
        """Create a new entity using the associated EntityManager."""
        try:
            detail = self._get_input_detail()
            self._entity_manager.create_entity(parent, detail)
            print(f"✅ {entity_name} created successfully.")
        except (ValidationError, LimitExceededError) as error:
            self._handle_error(error)

    def _update_entity_by_index(self, parent: object, entity_name: str) -> None:
        """Update an entity by selecting its index."""
        try:
            index, detail, status = self._get_entity_update_input(parent, entity_name)
            self._entity_manager.update_entity_by_index(parent, index, detail, status)
            print(f"✅ {entity_name} updated successfully.")
        except (NotFoundError, ValidationError, ValueError) as error:
            self._handle_error(error)

    def _delete_entity_by_index(self, parent: object, entity_name: str) -> None:
        """Delete an entity by selecting its index."""
        try:
            collection = self._entity_manager.get_collection(parent)
            self._view_entities(collection, entity_name)
            index = int(input(f"Enter {entity_name.lower()} number: ")) - 1
            self._entity_manager.remove_entity_by_index(parent, index)
            print(f"🗑️ {entity_name} deleted successfully.")
        except (NotFoundError, ValueError) as error:
            self._handle_error(error)

    def _handle_error(self, error: Exception) -> None:
        """Display formatted error."""
        if hasattr(error, "message") and callable(getattr(error, "message")):
            print(f"❌ {error.message()}")
        else:
            print(f"❌ {error}")
