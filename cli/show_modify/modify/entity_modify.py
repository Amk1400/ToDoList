from abc import ABC, abstractmethod
from typing import Optional, Union
from cli.base_menu import BaseMenu
from models.models import Project, Task, Option, Detail
from service.project_manager import ProjectManager
from service.task_manager import TaskManager
from datetime import datetime

class EntityModifyMenu(BaseMenu, ABC):
    """Abstract base menu to modify or delete an entity."""

    def __init__(
        self,
        manager: Union[ProjectManager, TaskManager],
        project: Optional[Project],
        entity: Union[Project, Task],
        parent_menu: Optional[BaseMenu] = None,
    ) -> None:
        self._manager = manager
        self._project = project
        self._entity = entity
        super().__init__("Modify Entity", parent_menu)

    def _setup_options(self) -> None:
        self._options = [
            Option("Edit", self._edit_entity),
            Option("Delete", self._delete_entity),
            Option("Back", self._go_back)
        ]

    @abstractmethod
    def _edit_entity(self) -> None:
        """Edit the entity; to be implemented in child class."""
        pass

    def _delete_entity(self) -> None:
        try:
            self._perform_delete()
        except Exception as e:
            print(f"❌ {e}")
        self._go_back()

    @abstractmethod
    def _perform_delete(self) -> None:
        """Delete the entity; to be implemented in child class."""
        pass
