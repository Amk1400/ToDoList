from typing import Optional
from cli.base_menu import BaseMenu
from cli.entity.management.task_management import TaskManagementMenu
from cli.entity.modify.entity_modify import EntityModifyMenu
from models.models import Project, Option
from service.project_manager import ProjectManager
from cli.entity.gateway.project_gateway import ProjectGateway


class ProjectModifyMenu(EntityModifyMenu):
    """Modify a project and optionally show its tasks."""

    def __init__(self, manager: ProjectManager, project: Project, parent_menu: Optional[BaseMenu] = None) -> None:
        super().__init__(manager, project, project, parent_menu)
        self._title = f"Modify Project: {project.detail.title}"

    def _setup_options(self) -> None:
        self._options = [
            Option("Edit Project", self._edit_entity),
            Option("Delete Project", self._delete_entity),
            Option("Show Tasks", self._show_tasks),
            Option("Back", self._go_back)
        ]

    def _edit_entity(self) -> None:
        try:
            ProjectGateway(self._manager).edit_entity(self._entity)
            print("✅ Updated successfully.")
        except Exception as e:
            self.handle_exception(e)
        self._go_back()

    def _perform_delete(self) -> None:
        try:
            ProjectGateway(self._manager).delete_entity(self._entity)
            print("✅ Deleted successfully.")
        except Exception as e:
            self.handle_exception(e)

    def _show_tasks(self) -> None:
        TaskManagementMenu(self._manager.get_task_manager(), self._entity, parent_menu=self).run()
