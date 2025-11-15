# cli/management/entity_management.py
from typing import Optional, Union
from cli.base_menu import BaseMenu
from models.models import Project, Task, Option
from service.project_manager import ProjectManager
from service.task_manager import TaskManager


class EntityManagementMenu(BaseMenu):
    """Base menu for entity management (projects or tasks)."""

    def __init__(
        self,
        manager: Union[ProjectManager, TaskManager],
        project: Optional[Project] = None,
        parent_menu: Optional[BaseMenu] = None,
    ) -> None:
        self._manager = manager
        self._project = project
        super().__init__("Entity Management", parent_menu)

    def _setup_options(self) -> None:
        self._options = []

        self.add_option(
            Option(
                title="Show & Modify",
                action=self._show_and_modify
            )
        )
        self.add_option(
            Option(
                title="Create",
                action=self._create_entity
            )
        )
        self.add_option(
            Option(
                title="Back",
                action=self._go_back
            )
        )

    def _show_and_modify(self) -> None:
        from cli.show_modify.show.entity_show import EntityShowMenu
        EntityShowMenu(self._manager, self._project, parent_menu=self).run()

    def _create_entity(self) -> None:
        # implement create logic or call another menu
        print("Create entity called")  # placeholder
