from typing import Optional
from cli.menus.base_menu import BaseMenu
from cli.gateway.project_gateway import ProjectGateway
from cli.gateway.task_gateway import TaskGateway
from cli.menus.entity.management.task_management import TaskManagementMenu
from cli.menus.entity.modify.entity_modify import EntityModifyMenu
from models.models import Project, Option


class ProjectModifyMenu(EntityModifyMenu[ProjectGateway]):
    """Modify a project and optionally show its tasks."""

    def __init__(
        self,
        gateway: ProjectGateway,
        project: Project,
        parent_menu: Optional[BaseMenu] = None
    ) -> None:
        super().__init__(gateway, None, project, parent_menu)
        self._project = project
        self._title = f"Modify Project: {project.detail.title}"

    def _add_show_tasks_option(self) -> None:
        self.add_option(Option("Show Tasks", self._show_tasks))

    def _show_tasks(self) -> None:
        task_gateway = TaskGateway(self._gateway.get_task_manager(self._project), self._entity)
        TaskManagementMenu(task_gateway, self._entity, parent_menu=self).run()