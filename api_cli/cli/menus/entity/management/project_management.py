from typing import Optional

from api_cli.cli.menus.base_menu import BaseMenu
from api_cli.gateway import ProjectGateway
from api_cli.cli.menus.entity.management.entity_management import EntityManagementMenu
from api_cli.cli.menus.entity.show.project_show import ProjectShowMenu


class ProjectManagementMenu(EntityManagementMenu):
    """Menu for managing projects."""

    def __init__(self, gateway: ProjectGateway, parent_menu: Optional[BaseMenu] = None):
        super().__init__(gateway, None, parent_menu)

    def _show_and_modify(self) -> None:
        ProjectShowMenu(self._gateway, parent_menu=self).run()