from datetime import datetime
from service.task_manager import TaskManager
from models.models import Detail, Project
from cli.base_menu import BaseMenu


class TaskManagementMenu(BaseMenu):
    """Menu for managing tasks inside a project."""

    def __init__(self, task_manager: TaskManager, project: Project, parent_menu: BaseMenu) -> None:
        """Initialize task menu.

        Args:
            task_manager (TaskManager): Task manager instance.
            project (Project): Target project.
            parent_menu (BaseMenu): Parent menu reference.
        """
        super().__init__(f"Task Menu: {project.detail.title}", parent_menu)
        self._task_manager = task_manager
        self._project = project
        self._setup_options()

    def _setup_options(self) -> None:
        """
        TODO first it should tell ushere
        its task management of what project?
        then
        i want 3 options
        1. show and modify which inherits from showentities and modify in entitymanagement
        2. create  which inherits from create entity in entity management
        3. back which enherits from back of basemenu
        """
        ...
