from abc import ABC, abstractmethod
from typing import Optional, Union
from cli.base_menu import BaseMenu
from models.models import Project, Task, Option
from service.project_manager import ProjectManager
from service.task_manager import TaskManager


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

    def _edit_entity(self) -> None:
        try:
            self._perform_edit()
            print(f"✅{self._entity.detail.title} Updated successfully.")
        except Exception as e:
            self.handle_exception(e)
        self._go_back()

    def _delete_entity(self) -> None:
        try:
            self._perform_delete()
            print(f"✅{self._entity.detail.title} Deleted successfully.")
        except Exception as e:
            self.handle_exception(e)
        self._go_back()

    @abstractmethod
    def _perform_edit(self) -> None:
        """Edit the entity; to be implemented in child class."""
        pass

    @abstractmethod
    def _perform_delete(self) -> None:
        """Delete the entity; to be implemented in child class."""
        pass

    def _setup_core_options(self) -> None:
        self.add_option(Option("Edit", self._edit_entity))
        self.add_option(Option("Delete", self._delete_entity))
        self._add_show_tasks_option()

    @abstractmethod
    def _add_show_tasks_option(self):
        raise NotImplementedError