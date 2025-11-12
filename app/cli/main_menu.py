from app.services.project_service import ProjectManager
from app.cli.base_menu import BaseMenu
from app.cli.project_menu import ProjectMenu

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
        """Open project menu.

        Raises:
            Exception: Any exception is handled via `_handle_error`.
        """
        try:
            ProjectMenu(self._project_manager, parent_menu=self).run()
        except Exception as error:
            self._handle_error(error)

    def _exit_program(self) -> None:
        """Exit.

        Effects:
            Stops the main menu loop and terminates the program.
        """
        self._is_running = False
        print("👋 Exiting application...")

    def _handle_error(self, error: Exception) -> None:
        """Display formatted error."""
        if hasattr(error, "message") and callable(getattr(error, "message")):
            print(f"❌ {error.message()}")
        else:
            print(f"❌ {error}")