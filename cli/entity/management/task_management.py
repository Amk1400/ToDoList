from cli.entity.gateway.task_gateway import TaskGateway
from cli.entity.management.entity_management import EntityManagementMenu
from cli.entity.show.task_show import TaskShowMenu
from models.models import Project
from service.task_manager import TaskManager


class TaskManagementMenu(EntityManagementMenu):
    """Menu for managing tasks within a project."""

    def __init__(self, manager: TaskManager, project: Project, parent_menu=None):
        manager.set_current_project(project)
        self._manager = manager
        self._project = project
        super().__init__(manager, project, parent_menu)

    def _show_and_modify(self) -> None:
        TaskShowMenu(self._manager, self._project, parent_menu=self).run()

    def _perform_creation(self) -> None:
        TaskGateway(self._manager, self._project).create_entity()