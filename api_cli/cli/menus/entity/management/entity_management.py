from abc import abstractmethod
from typing import Optional, TypeVar, Generic
from api_cli.cli.menus.base_menu import BaseMenu
from api_cli.gateway.entity_gateway import EntityGateway
from models.models import Option, Project

# Generic type برای Gateway
TGateway = TypeVar("TGateway", bound=EntityGateway)

class EntityManagementMenu(BaseMenu, Generic[TGateway]):
    """Base menu for entity management (projects or tasks)."""

    def __init__(
        self,
        gateway: TGateway,
        project: Optional[Project] = None,
        parent_menu: Optional[BaseMenu] = None,
    ) -> None:
        """
        Initialize entity management menu.

        Args:
            gateway (TGateway): Gateway instance (ProjectGateway or TaskGateway).
            project (Optional[Project]): Parent project if managing tasks.
            parent_menu (Optional[BaseMenu]): Parent menu for navigation.
        """
        self._gateway: TGateway = gateway
        self._project: Optional[Project] = project
        self._entity_type: str = "Task" if self._project else "Project"
        super().__init__(f"{self._entity_type} Management", parent_menu)

    def _setup_core_options(self) -> None:
        self.add_option(
            Option(f"Show & Modify {self._entity_type}s", self._show_and_modify)
        )
        self.add_option(Option(f"Create {self._entity_type}", self._create_entity))

    @abstractmethod
    def _show_and_modify(self) -> None:
        """Open the appropriate show/modify menu."""
        raise NotImplementedError("Override this method in subclass")

    def _create_entity(self) -> None:
        try:
            self._gateway.create_entity()
            print(f"✅ {self._entity_type} created successfully.")
        except Exception as e:
            self.handle_exception(e)
        self.run()