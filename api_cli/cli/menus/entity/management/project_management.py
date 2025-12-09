from typing import Optional

from api_cli.cli.menus.base_menu import BaseMenu
from api_cli.cli.menus.entity.management.entity_management import EntityManagementMenu
from api_cli.cli.menus.entity.show.project_show import ProjectShowMenu
from api_cli.gateway.project_gateway import ProjectGateway


class ProjectManagementMenu(EntityManagementMenu):
    """Project management menu."""

    def __init__(self, gateway: ProjectGateway,
                 parent_menu: Optional[BaseMenu] = None) -> None:
        """Initialize project management menu.

        Args:
            gateway (ProjectGateway): Project gateway.
            parent_menu (Optional[BaseMenu]): Parent menu reference.
        """
        super().__init__(gateway, None, parent_menu)

    def _show_and_modify(self) -> None:
        """Open project selection/modify menu."""
        ProjectShowMenu(self._gateway, parent_menu=self).run()
