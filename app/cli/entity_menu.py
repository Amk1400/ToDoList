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
        """Render a list of entities or raise NotFoundError if empty."""
        if not entities:
            raise NotFoundError(entity_name)#we can not pass list[0] because its empty
        for index, entity in enumerate(entities, start=1):
            title = getattr(entity.detail, "title", "Untitled")
            description = getattr(entity.detail, "description", "No description")
            extra = self._get_extra_info(entity)
            print(f"{index}. {title} {extra}- {description}")

    def _create_entity(self, create_callback: Callable[[Detail], None], entity_name: str) -> None:
        """Create a new entity."""
        try:
            detail = self._get_input_detail()
            create_callback(detail)
            print(f"✅ {entity_name} created successfully.")
        except (ValidationError, LimitExceededError) as error:
            self._handle_error(error)

    def _update_entity(
        self,
        entities: List[T],
        update_callback: Callable[[int, Detail], None],
        entity_name: str,
    ) -> None:
        """Update an entity."""
        try:
            self._view_entities(entities, entity_name)
            index = int(input(f"Enter {entity_name.lower()} number: ")) - 1
            detail = self._get_input_detail()
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
        """Delete an entity."""
        try:
            self._view_entities(entities, entity_name)
            index = int(input(f"Enter {entity_name.lower()} number: ")) - 1
            delete_callback(index)
            print(f"🗑️ {entity_name} deleted successfully.")
        except (NotFoundError, ValueError) as error:
            self._handle_error(error)

    def _handle_error(self, error: Exception) -> None:
        """Display formatted error."""
        if hasattr(error, "message") and callable(getattr(error, "message")):
            print(f"❌ {error.message()}")
        else:
            print(f"❌ {error}")