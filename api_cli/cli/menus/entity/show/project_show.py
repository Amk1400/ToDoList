from typing import Optional
from api_cli.cli.menus.base_menu import BaseMenu
from api_cli.cli.menus.entity.modify.project_modify import ProjectModifyMenu
from api_cli.cli.menus.entity.show.entity_show import EntityShowMenu
from api_cli.gateway.project_gateway import ProjectGateway
from models.models import Project


class ProjectShowMenu(EntityShowMenu):
    """Project selection menu."""

    def __init__(self, gateway: ProjectGateway,
                 parent_menu: Optional[BaseMenu] = None) -> None:
        """Initialize project show menu.

        Args:
            gateway (ProjectGateway): Gateway for project retrieval.
            parent_menu (Optional[BaseMenu]): Parent menu reference.
        """
        super().__init__(gateway, None, parent_menu, title="Select a Project to Modify")

    def _open_modify(self, project: Project) -> None:
        """Open project modification menu.

        Args:
            project (Project): Selected project instance.
        """
        ProjectModifyMenu(self._gateway, project, parent_menu=self).run()

    def _get_entity_name(self) -> str:
        """Return entity name."""
        return "Project"
