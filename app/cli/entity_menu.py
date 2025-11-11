from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Callable
from app.models.models import Detail
from app.cli.base_menu import BaseMenu
from app.exceptions.entity import NotFoundError, ValidationError, LimitExceededError

T = TypeVar("T")


class EntityMenu(BaseMenu, ABC, Generic[T]):
    """Abstract base menu for managing generic entities."""

    def __init__(self, title: str, parent_menu: BaseMenu) -> None:
        """
        Initialize the entity menu.

        Args:
            title (str): Menu title.
            parent_menu (BaseMenu): Parent menu for navigation.
        """
        super().__init__(title, parent_menu)
        self._setup_options()

    @abstractmethod
    def _setup_options(self) -> None:
        """Register menu-specific options."""
        raise NotImplementedError

    def _view_entities(self, entities: List[T], entity_name: str) -> None:
        """Render a list of entities.

        Args:
            entities (List[T]): Entities to display.
            entity_name (str): Name of the entity type.
        """
        if not entities:
            print(f"⚠ No {entity_name.lower()}s available.")
            return
        for index, entity in enumerate(entities, start=1):
            title = getattr(entity.detail, "title", "Untitled")
            description = getattr(entity.detail, "description", "No description")
            extra = self._get_extra_info(entity)
            print(f"{index}. {title} {extra}- {description}")

    @abstractmethod
    def _get_extra_info(self, entity: T) -> str:
        """Return any extra info to display beside the title.

        Args:
            entity (T): Entity instance.

        Returns:
            str: Formatted extra information (e.g., status).
        """
        raise NotImplementedError

    @staticmethod
    def _get_input_detail() -> Detail:
        """Collect title and description from user input.

        Returns:
            Detail: Detail object containing title and description.
        """
        title = input("Enter title: ").strip()
        description = input("Enter description: ").strip()
        return Detail(title=title, description=description)

    def _create_entity(self, create_callback: Callable[[Detail], None], entity_name: str) -> None:
        """Generic method to create an entity.

        Args:
            create_callback (Callable[[Detail], None]): Function that creates the entity given a Detail object.
            entity_name (str): Name of the entity type.
        """
        try:
            detail = self._get_input_detail()
            create_callback(detail)
            print(f"✅ {entity_name} created successfully.")
        except (ValidationError, LimitExceededError) as error:
            self._handle_error(error)

    def _handle_error(self, error: Exception) -> None:
        """Display a formatted error message.

        Args:
            error (Exception): The caught exception.
        """
        print(f"❌ {error}")

    def _delete_entity(
        self,
        entities: List[T],
        delete_callback: Callable[[int], None],
        entity_name: str,
    ) -> None:
        """Generic deletion of an entity from a list.

        Args:
            entities (List[T]): List of entities.
            delete_callback (Callable[[int], None]): Function to perform deletion by index.
            entity_name (str): Name of the entity type.
        """
        if not entities:
            print(f"⚠ No {entity_name.lower()}s available.")
            return

        self._view_entities(entities, entity_name)
        try:
            index = int(input(f"Enter {entity_name.lower()} number to delete: ")) - 1
            delete_callback(index)
            print(f"🗑️ {entity_name} deleted successfully.")
        except (NotFoundError, ValueError) as error:
            self._handle_error(error)
