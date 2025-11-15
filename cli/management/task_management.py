from cli.base_menu import BaseMenu
from models.models import Option, Project
from service.task_manager import TaskManager

class TaskManagementMenu(BaseMenu):
    """Menu for managing tasks inside a project."""

    def __init__(self, task_manager: TaskManager, project: Project, parent_menu: BaseMenu) -> None:
        self._task_manager = task_manager
        self._project = project
        super().__init__(f"Task Menu: {project.detail.title}", parent_menu)

    def _setup_options(self) -> None:
        self._options = [
            Option("Show & Modify Tasks", self._show_modify),
            Option("Create Task", self._create_task),
            Option("Back", self._go_back)
        ]

    def _show_modify(self) -> None:
        from cli.show_modify.entity_management import EntityManagementMenu
        EntityManagementMenu(self._task_manager, self._project, parent_menu=self).run()

    def _create_task(self) -> None:
        from models.models import Detail
        from datetime import datetime
        title = input("Enter task title: ").strip()
        desc = input("Enter task description: ").strip()
        deadline_str = input("Enter task deadline (YYYY-MM-DD): ").strip()
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            self._task_manager.add_task(self._project, Detail(title, desc), deadline)
            print("✅ Task created.")
        except Exception as e:
            print(f"❌ {e}")
        self.run()
