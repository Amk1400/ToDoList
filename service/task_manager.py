from typing import Optional, List, Any
from datetime import date
from core.config import AppConfig
from models.models import Detail, Task, Project
from service.base_manager import BaseManager
from core.validator import DeadlineValidator, StatusValidator

class TaskManager(BaseManager[Task]):
    """Handles task-level operations for a project."""

    def __init__(self, config: AppConfig) -> None:
        super().__init__(config)
        self.current_project: Optional[Project] = None
        self._entity_list: List[Task] = []

    def set_current_project(self, project: Project) -> None:
        self.current_project = project
        self._entity_list = project.tasks

    def entity_name(self) -> str:
        return "Task"

    def _create_entity_object(self, detail: Detail,
                              deadline: Optional[date] = None, status: Optional[str] = "todo") -> Task:
        status = "todo" if status is None else status
        return Task(detail=detail, deadline=deadline, status=status)

    def _update_deadline_and_status(self, deadline, entity, status):
        entity.deadline = deadline
        new_status = self.validate_status(status)
        entity.status = entity.status if new_status is None else new_status

    def _get_max_desc_length(self) -> int:
        return self._config.max_task_description_length

    def _get_max_title_length(self) -> int:
        return self._config.max_task_name_length

    def _get_max_count(self) -> int:
        return self._config.max_projects

    def _cascade_delete_tasks(self, entity) -> None:
        return None

    # ---------- Validator Methods ----------

    def validate_status(self, status: str) -> str:
        validator = StatusValidator()
        return validator.validate(status)

    def validate_deadline(self, deadline: date) -> None:
        validator = DeadlineValidator()
        validator.validate(str(deadline))
