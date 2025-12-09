from api_cli.cli.menus.base_menu import BaseMenu
from api_cli.gateway.project_gateway import ProjectGateway
from models.models import Option
from api_cli.cli.menus.entity.management.project_management import ProjectManagementMenu


class MainMenu(BaseMenu):
    """Main menu providing access to project management."""

    def __init__(self, project_gateway: ProjectGateway) -> None:
        self._project_gateway = project_gateway
        super().__init__("Main Menu")

    def _setup_options(self) -> None:
        self._options = []
        self.add_option(Option("Manage Projects", self._open_project_menu))
        self.add_option(Option("Exit", self._exit_program))

    def _setup_core_options(self) -> None:
        return None

    def _open_project_menu(self) -> None:
        ProjectManagementMenu(self._project_gateway, parent_menu=self).run()

    def _exit_program(self) -> None:
        print("👋 Exiting application...")
