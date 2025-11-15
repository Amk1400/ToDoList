from typing import Optional, Union
from cli.base_menu import BaseMenu
from models.models import Project, Task, Option, Detail
from service.project_manager import ProjectManager
from service.task_manager import TaskManager
from datetime import datetime

class EntityModifyMenu(BaseMenu):
    """Modify or delete a selected entity."""

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

    def _edit_entity(self) -> None:
        title = input("Enter new title: ").strip()
        description = input("Enter new description: ").strip()
        try:
            if isinstance(self._entity, Project):
                index = self._manager.get_all_projects().index(self._entity)
                self._manager.update_project(index, Detail(title, description))
            elif isinstance(self._entity, Task) and self._project:
                index = self._project.tasks.index(self._entity)
                deadline_str = input("Enter new deadline (YYYY-MM-DD) or leave empty: ").strip()
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date() if deadline_str else None
                self._manager.update_task(self._project, index, Detail(title, description), deadline)
            print("✅ Updated successfully.")
        except Exception as e:
            print(f"❌ {e}")
        self._go_back()

    def _delete_entity(self) -> None:
        try:
            if isinstance(self._entity, Project):
                index = self._manager.get_all_projects().index(self._entity)
                self._manager.remove_project(index)
            elif isinstance(self._entity, Task) and self._project:
                index = self._project.tasks.index(self._entity)
                self._manager.remove_task(self._project, index)
            print("✅ Deleted successfully.")
        except Exception as e:
            print(f"❌ {e}")
        self._go_back()
