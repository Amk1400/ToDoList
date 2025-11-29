from datetime import date
from typing import Optional, List
from core.config import AppConfig
from models.models import Detail, Task, Project
from repository.task_repository import TaskRepository
from service.entity_manager import EntityManager
from core.validator import StatusValidator, DeadlineValidator
from db.db import DataBase


class TaskManager(EntityManager[Task]):
    """Manager for task-level operations."""

    def __init__(self, config: AppConfig, db: DataBase) -> None:
        repository = TaskRepository(db)
        super().__init__(config, repository)
        self.current_project: Project | None = None

    def set_current_project(self, project: Project) -> None:
        """Set current project for task operations."""
        self.current_project = project

    def entity_name(self) -> str:
        return "Task"

    def _create_entity_object(
        self, detail: Detail, deadline: Optional[date] = None, status: str = "todo"
    ) -> Task:
        return Task(detail=detail, deadline=deadline, status=status)

    def _update_deadline_and_status_by_repo(self, deadline, entity: Task, status):
        entity.deadline = deadline
        entity.status = self.validate_status(status)

    def _get_max_desc_length(self) -> int:
        return self._config.max_task_description_length

    def _get_max_title_length(self) -> int:
        return self._config.max_task_name_length

    def _get_max_count(self) -> int:
        return self._config.max_tasks

    def _cascade_delete_tasks(self, entity) -> None:
        return None

    # ---------- Validators ----------

    def validate_status(self, status: str) -> str:
        validator = StatusValidator()
        return validator.validate(status)

    def validate_deadline(self, deadline: date) -> None:
        validator = DeadlineValidator()
        validator.validate(deadline)

    def get_repo_list(self) -> List[Task]:
        return self._repository.get_db_list(self.current_project)

    def _append_to_repository(self, entity: Task) -> None:
        """Append entity to repository."""
        self._repository.append_to_db(self.current_project,entity)