from typing import Optional

from api_cli.cli.menus.base_menu import BaseMenu
from api_cli.gateway.project_gateway import ProjectGateway
from api_cli.gateway.task_gateway import TaskGateway
from api_cli.cli.menus.entity.management.task_management import TaskManagementMenu
from api_cli.cli.menus.entity.modify.entity_modify import EntityModifyMenu
from models.models import Project, Option


class ProjectModifyMenu(EntityModifyMenu[ProjectGateway]):
    """Project modification menu."""

    def __init__(
            self,
            gateway: ProjectGateway,
            project: Project,
            parent_menu: Optional[BaseMenu] = None
    ) -> None:
        """Initialize project modify menu.

        Args:
            gateway (ProjectGateway): Project data gateway.
            project (Project): Selected project.
            parent_menu (Optional[BaseMenu]): Parent menu reference.
        """
        super().__init__(gateway, None, project, parent_menu)
        self._project = project
        self._title = f"Modify Project: {project.detail.title}"

    def _add_show_tasks_option(self) -> None:
        """Add option to show project tasks."""
        self.add_option(Option("Show Tasks", self._show_tasks))

    def _show_tasks(self) -> None:
        """Open task management menu."""
        task_gateway = TaskGateway(self._gateway.get_task_manager(self._project), self._entity)
        TaskManagementMenu(task_gateway, self._entity, parent_menu=self).run()
