from typing import Optional
from cli.base_menu import BaseMenu
from models.models import Project, Task
from service.task_manager import TaskManager
from cli.entity.show.entity_show import EntityShowMenu
from cli.entity.modify.task_modify import TaskModifyMenu

class TaskShowMenu(EntityShowMenu):
    """Show tasks of a project and open TaskModifyMenu."""

    def __init__(self, manager: TaskManager, project: Project, parent_menu: Optional[BaseMenu] = None) -> None:
        super().__init__(manager, project, parent_menu, title=f"Select a Task of Project '{project.detail.title}' to Modify")

    def _get_items(self):
        return self._project.tasks if self._project else []

    def _open_modify(self, task: Task) -> None:
        TaskModifyMenu(self._manager, self._project, task, parent_menu=self).run()
