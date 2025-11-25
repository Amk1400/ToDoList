from abc import ABC, abstractmethod
from typing import Optional, Union
from cli.base_menu import BaseMenu
from models.models import Project, Task, Option
from service.project_manager import ProjectManager
from service.task_manager import TaskManager

class EntityShowMenu(BaseMenu, ABC):
    """Abstract base menu to show entities and select one to modify."""

    def __init__(
        self,
        manager: Union[ProjectManager, TaskManager],
        project: Optional[Project] = None,
        parent_menu: Optional[BaseMenu] = None,
        title: str = "Show Entities",
    ) -> None:
        self._manager = manager
        self._project = project
        super().__init__(title, parent_menu)

    def _setup_options(self) -> None:
        self._options = []
        for entity in self._get_items():
            self.add_option(Option(
                entity,
                lambda e=entity: self._open_modify(e)
            ))
        self.add_option(Option("Back", self._go_back))

    @abstractmethod
    def _get_items(self):
        """Return the list of entities to display."""
        pass

    @abstractmethod
    def _open_modify(self, entity):
        """Open the correct modify menu for the entity."""
        pass
