from typing import Optional
from datetime import datetime
from cli.base_menu import BaseMenu
from cli.entity.show_modify.modify.entity_modify import EntityModifyMenu
from models.models import Project, Task, Option, Detail
from service.task_manager import TaskManager
from exceptions.validator import NonEmptyTextValidator, DeadlineValidator, StatusValidator


class TaskModifyMenu(EntityModifyMenu):
    """Modify a task."""

    def __init__(self, manager: TaskManager, project: Project, task: Task, parent_menu: Optional[BaseMenu] = None) -> None:
        super().__init__(manager, project, task, parent_menu)
        self._title = f"Modify Task: {task.detail.title}"

    def _setup_options(self) -> None:
        self._options = [
            Option("Edit Task", self._edit_entity),
            Option("Delete Task", self._delete_entity),
            Option("Back", self._go_back)
        ]

    def _fetch_title(self) -> str:
        while True:
            try:
                raw_title = input("Enter new title: ")
                validated = NonEmptyTextValidator(
                    raw_title,
                    max_len=self._manager._config.max_task_name_length,
                    field_name="Task title"
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
                    max_len=self._manager._config.max_task_description_length,
                    field_name="Task description"
                ).validate()
                return validated.value
            except Exception as e:
                self.handle_exception(e)

    def _fetch_detail(self) -> Detail:
        title = self._fetch_title()
        description = self._fetch_description()
        return Detail(title, description)

    def _fetch_status(self) -> Optional[str]:
        while True:
            try:
                raw_status = input("Enter new status (todo/doing/done) or leave empty: ")
                validated = StatusValidator(raw_status).validate()
                return validated.value
            except Exception as e:
                self.handle_exception(e)

    def _fetch_deadline(self) -> Optional[datetime.date]:
        while True:
            try:
                raw_deadline = input("Enter new deadline (YYYY-MM-DD) or leave empty: ")
                validated = DeadlineValidator(raw_deadline).validate()
                return validated.value
            except Exception as e:
                self.handle_exception(e)

    def _edit_entity(self) -> None:
        detail = self._fetch_detail()
        deadline = self._fetch_deadline()
        status = self._fetch_status()
        self._update_entity(detail, deadline, status)
        self._go_back()

    def _update_entity(self, detail: Detail, deadline: Optional[datetime.date], status: Optional[str]) -> None:
        try:
            self._manager.update_task(
                self._project,
                self._project.tasks.index(self._entity),
                detail,
                deadline,
                status
            )
            print("✅ Updated successfully.")
        except Exception as e:
            self.handle_exception(e)

    def _perform_delete(self) -> None:
        self._manager.remove_task(self._project, self._project.tasks.index(self._entity))
