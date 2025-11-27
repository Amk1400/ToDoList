from typing import Optional, List
from datetime import date
from core.config import AppConfig
from models.models import Detail, Task, Project
from service.base_manager import BaseManager


class TaskManager(BaseManager[Task]):
    """Handles task-level operations for a project."""

    def __init__(self, config: AppConfig) -> None:
        super().__init__(config)
        self.current_project: Optional[Project] = None
        self._entity_list: List[Task] = []

    def set_current_project(self, project: Project) -> None:
        self.current_project = project
        self._entity_list = project.tasks

    def update_task(
        self,
        idx: int,
        detail: Optional[Detail] = None,
        deadline: Optional[date] = None,
        status: Optional[str] = None,
    ) -> None:
        self._validate_entity_index(idx)
        task = self._entity_list[idx]

        if detail:
            self._update_entity_detail(task, detail)
        if deadline:
            self.validate_deadline(deadline)
            task.deadline = deadline
        if status:
            task.status = self.validate_status(status)

    def validate_status(self, status: str) -> str:
        allowed = {"todo", "doing", "done"}
        s = status.strip().lower()
        if s not in allowed:
            raise ValueError("Status must be one of: todo, doing, done.")
        return s

    def validate_deadline(self, deadline: date) -> None:
        from datetime import date as today
        if deadline < today.today():
            raise ValueError("Deadline cannot be in the past.")

    def _entity_name(self) -> str:
        return "Task"

    def _create_entity_object(self, detail: Detail, deadline: Optional[date] = None) -> Task:
        if deadline is None:
            raise ValueError("Deadline is required for Task.")
        return Task(detail=detail, deadline=deadline)

    def _get_max_desc_length(self) -> int:
        return self._config.max_task_description_length

    def _get_max_title_length(self) -> int:
        return self._config.max_task_name_length

    def assert_can_create(self) -> None:
        if not self.current_project:
            raise ValueError("Project must be selected before adding tasks.")
        self._assert_can_append(self._config.max_tasks)
