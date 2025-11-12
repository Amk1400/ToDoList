from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Callable
from app.models.models import Detail
from app.cli.base_menu import BaseMenu
from app.exceptions.entity import NotFoundError, ValidationError, LimitExceededError

T = TypeVar("T")


class EntityMenu(BaseMenu, ABC, Generic[T]):
    """Abstract base menu for managing entities."""

    def __init__(self, title: str, parent_menu: BaseMenu) -> None:
        """Initialize the entity menu.

        Args:
            title (str): Menu title.
            parent_menu (BaseMenu): Parent menu for navigation.
        """
        super().__init__(title, parent_menu)
        self._setup_options()

    @abstractmethod
    def _setup_options(self) -> None:
        """Register menu options."""
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
        """Return entity-specific info.

        Args:
            entity (T): Entity instance.

        Returns:
            str: Additional info beside the title.
        """
        raise NotImplementedError

    @staticmethod
    def _get_input_detail() -> Detail:
        """Collect user input for detail.

        Returns:
            Detail: Title and description from user input.
        """
        title = input("Enter title: ").strip()
        description = input("Enter description: ").strip()
        return Detail(title=title, description=description)

    def _create_entity(self, create_callback: Callable[[Detail], None], entity_name: str) -> None:
        """Create a new entity.

        Args:
            create_callback (Callable[[Detail], None]): Callback to create the entity.
            entity_name (str): Name of the entity.
        """
        try:
            detail = self._get_input_detail()
            create_callback(detail)
            print(f"✅ {entity_name} created successfully.")
        except (ValidationError, LimitExceededError) as error:
            self._handle_error(error)

    def _update_entity(self,
        entities: List[T],
        update_callback: Callable[[int, Detail], None],
        entity_name: str,
    ) -> None:
        """Update an entity.

        Args:
            entities (List[T]): List of entities.
            update_callback (Callable[[int, Detail], None]): Update callback.
            entity_name (str): Entity type name.

        Raises:
            NotFoundError: If index invalid.
            ValidationError: If validation fails.
        """
        if not entities:
            print(f"⚠ No {entity_name.lower()}s available.")
            return

        self._view_entities(entities, entity_name)
        try:
            index = int(input(f"Enter {entity_name.lower()} number: ")) - 1
            title = input("Enter new title: ").strip()
            description = input("Enter new description: ").strip()
            detail = Detail(title=title, description=description)
            update_callback(index, detail)
            print(f"✅ {entity_name} updated successfully.")
        except (NotFoundError, ValidationError, ValueError) as error:
            self._handle_error(error)

    def _delete_entity(
        self,
        entities: List[T],
        delete_callback: Callable[[int], None],
        entity_name: str,
    ) -> None:
        """Delete an entity.

        Args:
            entities (List[T]): Entities list.
            delete_callback (Callable[[int], None]): Callback to delete entity.
            entity_name (str): Name of the entity type.

        Raises:
            NotFoundError: If index invalid.
        """
        if not entities:
            print(f"⚠ No {entity_name.lower()}s available.")
            return

        self._view_entities(entities, entity_name)
        try:
            index = int(input(f"Enter {entity_name.lower()} number: ")) - 1
            delete_callback(index)
            print(f"🗑️ {entity_name} deleted successfully.")
        except (NotFoundError, ValueError) as error:
            self._handle_error(error)

    def _handle_error(self, error: Exception) -> None:
        """Display formatted error.

        Args:
            error (Exception): Exception to handle.
        """
        print(f"❌ {error}")
