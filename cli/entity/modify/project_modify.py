from typing import Optional
from cli.base_menu import BaseMenu
from cli.entity.management.task_management import TaskManagementMenu
from cli.entity.modify.entity_modify import EntityModifyMenu
from models.models import Project, Option, Detail
from service.project_manager import ProjectManager
from exceptions.validator import NonEmptyTextValidator


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

    def _fetch_title(self) -> str:
        while True:
            try:
                raw_title = input("Enter new title: ")
                validated = NonEmptyTextValidator(
                    raw_title,
                    max_len=self._manager._config.max_project_name_length,
                    field_name="Project title"
                ).validate()
                return validated.value
            except Exception as e:
                self.handle_exception(e)

    def _fetch_description(self) -> str:
        while True:
            try:
                raw_desc = input("Enter new description: ")
                validated = NonEmptyTextValidator(
                    raw_desc,
                    max_len=self._manager._config.max_project_description_length,
                    field_name="Project description"
                ).validate()
                return validated.value
            except Exception as e:
                self.handle_exception(e)

    def _fetch_detail(self) -> Detail:
        title = self._fetch_title()
        description = self._fetch_description()
        return Detail(title, description)

    def _edit_entity(self) -> None:
        detail = self._fetch_detail()
        self._update_entity(detail)
        self._go_back()

    def _update_entity(self, detail: Detail) -> None:
        try:
            self._manager.update_project(
                self._manager.get_all_projects().index(self._entity),
                detail
            )
            print("✅ Updated successfully.")
        except Exception as e:
            self.handle_exception(e)

    def _perform_delete(self) -> None:
        self._manager.remove_project(self._manager.get_all_projects().index(self._entity))

    def _show_tasks(self) -> None:
        TaskManagementMenu(self._manager.get_task_manager(), self._entity, parent_menu=self).run()
