from typing import Optional
from cli.base_menu import BaseMenu
from cli.entity.modify.entity_modify import EntityModifyMenu
from models.models import Project, Task, Option
from service.task_manager import TaskManager
from cli.entity.gateway.task_gateway import TaskGateway


class TaskModifyMenu(EntityModifyMenu):
    """Modify a task."""

    def __init__(self, manager: TaskManager, project: Project, task: Task, parent_menu: Optional[BaseMenu] = None) -> None:
        super().__init__(manager, project, task, parent_menu)
        self._title = f"Modify Task: {task.detail.title}"

    def _add_show_tasks_option(self) -> None:
        return None

    def _perform_edit(self) -> None:
        TaskGateway(self._manager, self._project).edit_entity(self._entity)

    def _perform_delete(self) -> None:
        TaskGateway(self._manager, self._project).delete_entity(self._entity)