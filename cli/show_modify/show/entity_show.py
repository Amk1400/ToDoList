from typing import Optional, Union
from cli.base_menu import BaseMenu
from models.models import Project, Task, Option
from service.project_manager import ProjectManager
from service.task_manager import TaskManager
from cli.show_modify.modify.entity_modify import EntityModifyMenu

class EntityShowMenu(BaseMenu):
    """Show entities and select one to modify."""

    def __init__(
        self,
        manager: Union[ProjectManager, TaskManager],
        project: Optional[Project] = None,
        parent_menu: Optional[BaseMenu] = None,
    ) -> None:
        self._manager = manager
        self._project = project
        super().__init__("Show Entities", parent_menu)

    def _setup_options(self) -> None:
        items = self._get_items()
        self._options = []
        for idx, item in enumerate(items, start=1):
            self._options.append(Option(
                f"{item.detail.title} - {item.detail.description}",
                lambda i=item: EntityModifyMenu(self._manager, self._project, i, parent_menu=self).run()
            ))
        self._options.append(Option("Back", self._go_back))

    def _get_items(self):
        if isinstance(self._manager, ProjectManager):
            return self._manager.get_all_projects()
        elif isinstance(self._manager, TaskManager) and self._project:
            return self._project.tasks
        return []
