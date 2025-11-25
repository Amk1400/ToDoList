from service.project_manager import ProjectManager
from cli.base_menu import BaseMenu
from cli.entity.management.project_management import ProjectManagementMenu
from models.models import Option

class MainMenu(BaseMenu):
    """Main menu providing access to project and task management."""

    def __init__(self, project_manager: ProjectManager) -> None:
        self._project_manager = project_manager
        super().__init__("Main Menu")

    def _setup_options(self) -> None:
        self._options = [
            Option("Manage Projects", self._open_project_menu),
            Option("Exit", self._exit_program)
        ]

    def _open_project_menu(self) -> None:
        ProjectManagementMenu(self._project_manager, parent_menu=self).run()

    def _exit_program(self) -> None:
        print("👋 Exiting application...")
