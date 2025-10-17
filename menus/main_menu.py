from managers.project_manager import ProjectManager
from menus.base_menu import BaseMenu
from menus.project_menu import ProjectMenu


class MainMenu(BaseMenu):
    """Main menu for managing projects and tasks."""

    def __init__(self, project_manager: ProjectManager) -> None:
        """Initialize main menu with dependencies."""
        super().__init__("Main Menu")
        self._project_manager = project_manager
        self._setup_options()

    def _setup_options(self) -> None:
        """Define menu options."""
        self.add_option("1", self._open_project_menu)
        self.add_option("2", self._exit_program)

    def _open_project_menu(self) -> None:
        """Open project management menu."""
        ProjectMenu(self._project_manager, parent_menu=self).run()

    def _exit_program(self) -> None:
        """Exit program."""
        self._is_running = False
        print("Exiting application...")
