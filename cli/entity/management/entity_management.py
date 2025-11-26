from typing import Optional
from cli.base_menu import BaseMenu
from models.models import Project, Option


class EntityManagementMenu(BaseMenu):
    """Base menu for entity management (projects or tasks)."""

    def __init__(
        self,
        manager,
        project: Optional[Project] = None,
        parent_menu: Optional[BaseMenu] = None,
    ) -> None:
        """
        Initialize entity management menu.

        Args:
            manager: ProjectManager or TaskManager instance.
            project (Optional[Project]): Parent project if managing tasks.
            parent_menu (Optional[BaseMenu]): Parent menu.
        """
        self._manager = manager
        self._project = project

        self._entity = "Task" if self._project else "Project"
        super().__init__(f"{self._entity} Management", parent_menu)

    def _setup_core_options(self) -> None:
        self.add_option(Option(f"Show & Modify {self._entity}s", self._show_and_modify))
        self.add_option(Option(f"Create {self._entity}", self._create_entity))

    def _show_and_modify(self) -> None:
        raise NotImplementedError("Override this method in subclass")

    def _create_entity(self) -> None:
        """
        Create a new entity by delegating to Gateway.
        Subclasses override to choose the correct Gateway.
        """
        raise NotImplementedError("Override this method in subclass")
