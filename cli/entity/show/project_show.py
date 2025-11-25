from typing import Optional
from cli.base_menu import BaseMenu
from models.models import Project
from service.project_manager import ProjectManager
from cli.entity.show.entity_show import EntityShowMenu
from cli.entity.modify.project_modify import ProjectModifyMenu

class ProjectShowMenu(EntityShowMenu):
    """Show all projects and open ProjectModifyMenu."""

    def __init__(self, manager: ProjectManager, parent_menu: Optional[BaseMenu] = None) -> None:
        super().__init__(manager, parent_menu=parent_menu, title="Select a Project to Modify")

    def _get_items(self):
        return self._manager.get_all_projects()

    def _open_modify(self, project: Project) -> None:
        ProjectModifyMenu(self._manager, project, parent_menu=self).run()
