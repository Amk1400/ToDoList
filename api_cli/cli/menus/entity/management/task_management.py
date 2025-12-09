from typing import Optional
from api_cli.cli.menus.base_menu import BaseMenu
from api_cli.gateway.task_gateway import TaskGateway
from api_cli.cli.menus.entity.management.entity_management import EntityManagementMenu
from api_cli.cli.menus.entity.show.task_show import TaskShowMenu
from models.models import Project

class TaskManagementMenu(EntityManagementMenu):
    """Menu for managing tasks within a project."""

    def __init__(self, gateway: TaskGateway, project: Project, parent_menu: Optional[BaseMenu] = None):
        self._gateway: TaskGateway = gateway
        self._project: Project = project
        self._gateway.set_current_project(self._project)
        super().__init__(self._gateway, self._project, parent_menu)

    def _show_and_modify(self) -> None:
        TaskShowMenu(self._gateway, self._project, parent_menu=self).run()