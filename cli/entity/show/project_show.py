from typing import Optional
from cli.base_menu import BaseMenu
from cli.entity.gateway.project_gateway import ProjectGateway
from cli.entity.modify.project_modify import ProjectModifyMenu
from cli.entity.show.entity_show import EntityShowMenu
from models.models import Project


class ProjectShowMenu(EntityShowMenu):
    """Show all projects and open ProjectModifyMenu."""

    def __init__(self, gateway: ProjectGateway, parent_menu: Optional[BaseMenu] = None):
        super().__init__(gateway, None, parent_menu, title="Select a Project to Modify")

    def _open_modify(self, project: Project) -> None:
        ProjectModifyMenu(self._gateway, project, parent_menu=self).run()
