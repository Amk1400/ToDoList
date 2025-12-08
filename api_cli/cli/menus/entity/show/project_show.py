from typing import Optional
from api_cli.cli.menus.base_menu import BaseMenu
from api_cli.gateway import ProjectGateway
from api_cli.cli.menus.entity.modify.project_modify import ProjectModifyMenu
from api_cli.cli.menus.entity.show.entity_show import EntityShowMenu
from models.models import Project


class ProjectShowMenu(EntityShowMenu):
    """Show all projects and open ProjectModifyMenu."""

    def __init__(self, gateway: ProjectGateway, parent_menu: Optional[BaseMenu] = None):
        super().__init__(gateway, None, parent_menu, title="Select a Project to Modify")

    def _open_modify(self, project: Project) -> None:
        ProjectModifyMenu(self._gateway, project, parent_menu=self).run()

    def _get_entity_name(self) -> str:
        return "Project"