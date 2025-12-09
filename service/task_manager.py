from datetime import date
from typing import Optional, List
from core.config import AppConfig
from models.models import Detail, Task, Project
from repository.task_repository import TaskRepository
from service.entity_manager import EntityManager
from core.validator import StatusValidator, DeadlineValidator

class TaskManager(EntityManager[Task]):
    """Manager for task-level operations."""

    def __init__(self, config: AppConfig, db, current_project: Optional[Project] = None) -> None:
        repository = TaskRepository(db)
        super().__init__(config, repository)
        self._parent_project: Optional[Project] = None
        if current_project:
            self.set_parent_project(current_project)

    def set_parent_project(self, project: Project) -> None:
        self._parent_project = project

    def entity_name(self) -> str:
        return "Task"

    def create_entity_object(
        self, detail: Detail, deadline: Optional[date] = None, status: Optional[str] = "todo"
    ) -> Task:
        if status is None:
            status = "todo"
        return Task(detail=detail, deadline=deadline, status=status)

    def _update_deadline_and_status_by_repo(self, deadline: Optional[date], entity: Task, status: Optional[str]):
        if deadline is not None:
            entity.deadline = deadline
        if status is not None:
            entity.status = self.validate_status(status)

    def _get_max_desc_length(self) -> int:
        return self._config.max_task_description_length

    def _get_max_title_length(self) -> int:
        return self._config.max_task_name_length

    def _get_max_count(self) -> int:
        return self._config.max_tasks

    def remove_entity_object(self, entity: Task) -> None:
        """Remove entity and handle cascade deletes if needed."""
        self._remove_from_repository(entity, self._parent_project)

    # ---------- Validators ----------

    def validate_status(self, status: str) -> str:
        validator = StatusValidator()
        return validator.validate(status)

    def validate_deadline(self, deadline: date) -> None:
        validator = DeadlineValidator()
        validator.validate(deadline)

    def get_repo_list(self) -> List[Task]:
        if self._parent_project is None:
            raise ValueError("Current project is not set for TaskManager.")
        return self._repository.get_db_list(self._parent_project)

    def _append_to_repository(self, entity: Task) -> None:
        if self._parent_project is None:
            raise ValueError("Current project is not set for TaskManager.")
        self._repository.append_to_db(entity, self._parent_project)

    def _remove_from_repository(self, entity: Task, parent_project: Optional[Project] = None) -> None:
        if parent_project is None:
            raise ValueError("Parent project must be provided for tasks.")
        self._repository.remove_from_db(entity, parent_project)

    def get_parent_project(self) -> Project:
        return self._parent_project
