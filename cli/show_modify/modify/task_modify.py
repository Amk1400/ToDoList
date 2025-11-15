from typing import Optional
from cli.base_menu import BaseMenu
from models.models import Project, Task
from service.task_manager import TaskManager
from cli.show_modify.modify.entity_modify import EntityModifyMenu
from datetime import datetime

class TaskModifyMenu(EntityModifyMenu):
    """Modify a task."""

    def __init__(self, manager: TaskManager, project: Project, task: Task, parent_menu: Optional[BaseMenu] = None) -> None:
        super().__init__(manager, project, task, parent_menu)
        self._title = f"Modify Task: {task.detail.title}"

    def _edit_entity(self) -> None:
        detail = self._fetch_detail()
        deadline = self._fetch_deadline()
        status = self._fetch_status()

        self._update_entity(deadline, detail, status)
        self._go_back()

    def _fetch_status(self):
        try:
            status_input = input("Enter new status (todo/doing/done) or leave empty: ").strip().lower()
            status = status_input if status_input else None
            if status and status not in {"todo", "doing", "done"}:
                raise ValueError("Status must be one of: todo, doing, done.")
        except Exception as e:
            print(f"❌ {e}")
            return self._fetch_status()
        return status

    def _fetch_deadline(self):
        try:
            deadline_str = input("Enter new deadline (YYYY-MM-DD) or leave empty: ").strip()
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date() if deadline_str else None
            if deadline:
                self._manager._validate_deadline(deadline)
        except Exception as e:
            print(f"❌ Invalid deadline: {e}")
            return self._fetch_deadline()
        return deadline

    def _update_entity(self, deadline, detail, status):
        try:
            self._manager.update_task(
                self._project,
                self._project.tasks.index(self._entity),
                detail,
                deadline,
                status
            )
            print("✅ Updated successfully.")
        except Exception as e:
            print(f"❌ {e}")

    def _perform_delete(self) -> None:
        self._manager.remove_task(self._project, self._project.tasks.index(self._entity))