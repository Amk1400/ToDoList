from api_cli.cli.menus.base_menu import BaseMenu
from api_cli.gateway.project_gateway import ProjectGateway
from models.models import Option
from api_cli.cli.menus.entity.management.project_management import ProjectManagementMenu


class MainMenu(BaseMenu):
    """Main menu entrypoint."""

    def __init__(self, project_gateway: ProjectGateway) -> None:
        """Initialize main menu.

        Args:
            project_gateway (ProjectGateway): Gateway for project operations.
        """
        self._project_gateway = project_gateway
        super().__init__("Main Menu")

    def _setup_options(self) -> None:
        """Configure menu options."""
        self._options = []
        self.add_option(Option("Manage Projects", self._open_project_menu))
        self.add_option(Option("Exit", self._exit_program))

    def _setup_core_options(self) -> None:
        """Set core options."""
        return None

    def _open_project_menu(self) -> None:
        """Open project management menu."""
        ProjectManagementMenu(self._project_gateway, parent_menu=self).run()

    @staticmethod
    def _exit_program() -> None:
        """Terminate application."""
        print("👋 Exiting application...")
