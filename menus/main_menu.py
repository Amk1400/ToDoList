from managers.project_manager import ProjectManager
from menus.base_menu import BaseMenu
from menus.project_menu import ProjectMenu


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
        """Define and register menu options."""
        self.add_option("1", self._open_project_menu)
        self.add_option("2", self._exit_program)

    def _open_project_menu(self) -> None:
        """Navigate to the project management menu.

        Raises:
            Exception: If the project menu fails to open.
        """
        try:
            ProjectMenu(self._project_manager, parent_menu=self).run()
        except Exception as error:
            print(f"❌ Error while opening project menu: {error}")

    def _exit_program(self) -> None:
        """Exit the application safely.

        Effects:
            Stops the main menu loop and terminates the program.
        """
        self._is_running = False
        print("👋 Exiting application...")
