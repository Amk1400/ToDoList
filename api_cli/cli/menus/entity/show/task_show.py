from typing import Optional

from api_cli.cli.menus.base_menu import BaseMenu
from api_cli.gateway.task_gateway import TaskGateway
from api_cli.cli.menus.entity.modify.task_modify import TaskModifyMenu
from api_cli.cli.menus.entity.show.entity_show import EntityShowMenu
from models.models import Project, Task


class TaskShowMenu(EntityShowMenu):
    """Task selection menu."""

    def __init__(self, gateway: TaskGateway, project: Project,
                 parent_menu: Optional[BaseMenu] = None) -> None:
        """Initialize task show menu.

        Args:
            gateway (TaskGateway): Task data gateway.
            project (Project): Project containing tasks.
            parent_menu (Optional[BaseMenu]): Parent menu reference.
        """
        super().__init__(
            gateway,
            project,
            parent_menu,
            title=f"Select a Task of Project '{project.detail.title}' to Modify"
        )

    def _open_modify(self, task: Task) -> None:
        """Open modification menu for a task.

        Args:
            task (Task): Selected task for modification.
        """
        TaskModifyMenu(self._gateway, self._project, task, parent_menu=self).run()

    def _get_entity_name(self) -> str:
        """Return entity name."""
        return "Task"
