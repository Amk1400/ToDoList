from typing import Optional, Union
from cli.base_menu import BaseMenu
from models.models import Project, Task, Option
from service.project_manager import ProjectManager
from service.task_manager import TaskManager
from cli.show_modify.show.entity_show import EntityShowMenu
from models.models import Detail

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
        self.add_option(Option("Show & Modify", self._show_and_modify))
        self.add_option(Option("Create", self._create_entity))
        self.add_option(Option("Back", self._go_back))

    def _show_and_modify(self) -> None:
        EntityShowMenu(self._manager, self._project, parent_menu=self).run()#TODO it should run taskshow if it is called by "show tasks and modify in modify menu of a project" else it should run project show

    def _create_entity(self) -> None:
        from datetime import datetime
        title = input("Enter title: ").strip()
        description = input("Enter description: ").strip()
        try:
            if isinstance(self._manager, ProjectManager):
                self._manager.create_project(Detail(title, description))
                print("✅ Project created.")
            elif isinstance(self._manager, TaskManager) and self._project:
                deadline_str = input("Enter task deadline (YYYY-MM-DD): ").strip()
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
                self._manager.add_task(self._project, Detail(title, description), deadline)
                print("✅ Task created.")
        except Exception as e:
            print(f"❌ {e}")
        self.run()
