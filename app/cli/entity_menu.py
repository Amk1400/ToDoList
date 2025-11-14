from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from app.models.models import Detail, Status
from app.cli.base_menu import BaseMenu
from app.exceptions.entity import NotFoundError

T = TypeVar("T")


class EntityMenu(BaseMenu, ABC, Generic[T]):
    """Abstract menu for entity management."""

    def __init__(self, title: str, parent_menu: Optional[BaseMenu] = None) -> None:
        """Initialize the entity menu.

        Args:
            title (str): Menu title.
            parent_menu (Optional[BaseMenu]): Parent menu reference.
        """
        super().__init__(title, parent_menu)
        self._setup_options()

    @abstractmethod
    def _setup_options(self) -> None:
        """Register menu options."""
        raise NotImplementedError

    def _get_input_detail(self) -> Detail:
        """Collect user input for detail."""
        title = input("Enter title: ").strip()
        description = input("Enter description: ").strip()
        return Detail(title=title, description=description)

    def _view_entities(self, entities: List[T], entity_name: str) -> None:
        """Display entities or raise NotFoundError."""
        if not entities:
            raise NotFoundError(entity_name)
        for index, entity in enumerate(entities, start=1):
            print(f"{index}. {entity}")

    def _handle_error(self, error: Exception) -> None:
        """Display error message."""
        print(f"❌ {error}")