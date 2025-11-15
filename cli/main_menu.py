from service.project_manager import ProjectManager
from cli.base_menu import BaseMenu
from cli.management.project_management import ProjectManagementMenu


class MainMenu(BaseMenu):
    """Main menu providing access to project and task management."""

    def __init__(self, project_manager: ProjectManager) -> None:
        """Initialize the main menu.

        Args:
            project_manager (ProjectManager): Handles project-related operations.
        """
        super().__init__("Main Menu")
        self._project_manager = project_manager
        self._setup_options()

    def _setup_options(self) -> None:
        """
        TODO here i want two options
        1. open project management menu
        2. exit
        """
        ...

    def _open_project_menu(self) -> None:
        """project menu.

        Raises:
            Exception: If the project menu fails to open.
        """
        try:
            ProjectManagementMenu(self._project_manager, parent_menu=self).run()
        except Exception as error:
            print(f"❌ Error while opening project menu: {error}")

    def _exit_program(self) -> None:
        """Exit.

        Effects:
            Stops the main menu loop and terminates the program.
        """
        self._is_running = False
        print("👋 Exiting application...")
