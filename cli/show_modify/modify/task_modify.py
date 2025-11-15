from typing import Optional
from cli.base_menu import BaseMenu
from models.models import Project, Task, Option, Detail
from service.task_manager import TaskManager
from cli.show_modify.modify.entity_modify import EntityModifyMenu
from datetime import datetime

class TaskModifyMenu(EntityModifyMenu):
    """Modify a task."""

    def __init__(self, manager: TaskManager, project: Project, task: Task, parent_menu: Optional[BaseMenu] = None) -> None:
        super().__init__(manager, project, task, parent_menu)
        self._title = f"Modify Task: {task.detail.title}"

    def _edit_entity(self) -> None:
        title = input("Enter new title: ").strip()
        description = input("Enter new description: ").strip()
        deadline_str = input("Enter new deadline (YYYY-MM-DD) or leave empty: ").strip()
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date() if deadline_str else None
        try:
            self._manager.update_task(
                self._project,
                self._project.tasks.index(self._entity),
                Detail(title, description),
                deadline
            )
            print("✅ Updated successfully.")
        except Exception as e:
            print(f"❌ {e}")
        self._go_back()

    def _perform_delete(self) -> None:
        self._manager.remove_task(self._project, self._project.tasks.index(self._entity))
