from typing import Optional

from cli.base_menu import BaseMenu
from cli.entity.gateway.project_gateway import ProjectGateway
from cli.entity.management.entity_management import EntityManagementMenu
from cli.entity.show.project_show import ProjectShowMenu


class ProjectManagementMenu(EntityManagementMenu):
    """Menu for managing projects."""

    def __init__(self, gateway: ProjectGateway, parent_menu: Optional[BaseMenu] = None):
        super().__init__(gateway, None, parent_menu)

    def _show_and_modify(self) -> None:
        ProjectShowMenu(self._gateway, parent_menu=self).run()