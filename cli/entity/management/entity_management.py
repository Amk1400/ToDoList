from abc import abstractmethod
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

        self._entity_type = "Task" if self._project else "Project"
        super().__init__(f"{self._entity_type} Management", parent_menu)

    def _setup_core_options(self) -> None:
        self.add_option(Option(f"Show & Modify {self._entity_type}s", self._show_and_modify))
        self.add_option(Option(f"Create {self._entity_type}", self._create_entity))

    def _show_and_modify(self) -> None:
        raise NotImplementedError("Override this method in subclass")

    def _create_entity(self) -> None:
        try:
            self._perform_creation()
            print(f"✅{self._entity_type} created successfully.")
        except Exception as e:
            self.handle_exception(e)
        self.run()

    @abstractmethod
    def _perform_creation(self):
        raise NotImplementedError("Override this method in subclass")