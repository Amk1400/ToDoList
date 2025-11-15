from typing import Optional
from cli.base_menu import BaseMenu
from models.models import Project, Option, Detail
from service.project_manager import ProjectManager
from cli.show_modify.modify.entity_modify import EntityModifyMenu
from cli.management.task_management import TaskManagementMenu

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
        detail = self._fetch_detail()
        self._update_entity(detail)
        self._go_back()

    def _update_entity(self, detail):
        try:
            self._manager.update_project(
                self._manager.get_all_projects().index(self._entity),
                detail
            )
            print("✅ Updated successfully.")
        except Exception as e:
            print(f"❌ Error updating project: {e}")

    def _perform_delete(self) -> None:
        self._manager.remove_project(self._manager.get_all_projects().index(self._entity))

    def _show_tasks(self) -> None:
        TaskManagementMenu(self._manager.get_task_manager(), self._entity, parent_menu=self).run()
