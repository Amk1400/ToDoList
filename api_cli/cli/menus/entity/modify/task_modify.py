from typing import Optional

from api_cli.cli.menus.base_menu import BaseMenu
from api_cli.gateway.task_gateway import TaskGateway
from api_cli.cli.menus.entity.modify.entity_modify import EntityModifyMenu
from models.models import Project, Task


class TaskModifyMenu(EntityModifyMenu[TaskGateway]):
    """Task modification menu."""

    def __init__(self, gateway: TaskGateway, project: Project,
                 task: Task, parent_menu: Optional[BaseMenu] = None) -> None:
        """Initialize task modify menu.

        Args:
            gateway (TaskGateway): Task data gateway.
            project (Project): Parent project.
            task (Task): Selected task.
            parent_menu (Optional[BaseMenu]): Parent menu reference.
        """
        super().__init__(gateway, project, task, parent_menu)
        self._title = f"Modify Task: {task.detail.title}"

    def _add_show_tasks_option(self) -> None:
        """Skip task listing option."""
        return None
