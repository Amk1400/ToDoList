from typing import Optional

from api_cli.cli.menus.base_menu import BaseMenu
from api_cli.gateway.task_gateway import TaskGateway
from api_cli.cli.menus.entity.modify.task_modify import TaskModifyMenu
from api_cli.cli.menus.entity.show.entity_show import EntityShowMenu
from models.models import Project, Task


class TaskShowMenu(EntityShowMenu):
    """Show tasks of a project and open TaskModifyMenu."""

    def __init__(self, gateway: TaskGateway, project: "Project", parent_menu: Optional[BaseMenu] = None):
        super().__init__(gateway, project, parent_menu, title=f"Select a Task of Project '{project.detail.title}' to Modify")

    def _open_modify(self, task: Task) -> None:
        TaskModifyMenu(self._gateway, self._project, task, parent_menu=self).run()

    def _get_entity_name(self) -> str:
        return "Task"