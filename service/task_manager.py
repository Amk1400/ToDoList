from typing import Optional
from datetime import date
from core.config import AppConfig
from models.models import Detail, Task, Project
from service.base_manager import BaseManager


class TaskManager(BaseManager[Task]):
    """Handles task-level operations for a project."""

    def __init__(self, config: AppConfig) -> None:
        super().__init__(config)
        self.current_project: Optional[Project] = None  # Must be set before adding/editing tasks

    def add_task(self, project: Project, detail: Detail, deadline: date) -> None:
        self._validate(detail)
        self._validate_deadline(deadline)
        if len(project.tasks) >= self._config.max_tasks:
            raise OverflowError("Maximum number of tasks reached.")
        project.tasks.append(Task(detail=detail, deadline=deadline))

    def update_task(
        self,
        project: Project,
        task_idx: int,
        detail: Optional[Detail] = None,
        deadline: Optional[date] = None,
        status: Optional[str] = None,
    ) -> None:
        if not (0 <= task_idx < len(project.tasks)):
            raise IndexError("Invalid task index.")
        task = project.tasks[task_idx]

        if detail:
            self._validate(detail)
            self._update_entity_detail(task, detail)
        if deadline:
            self._validate_deadline(deadline)
            task.deadline = deadline
        if status:
            if status not in {"todo", "doing", "done"}:
                raise ValueError("Invalid status. Must be todo/doing/done.")
            task.status = status

    def _entity_name(self) -> str:
        return "Task"

    def _create_entity(self, detail: Detail) -> Task:
        raise NotImplementedError("Use add_task() with a project and deadline.")

    def _validate(self, detail: Detail) -> None:
        max_name = self._config.max_task_name_length
        max_desc = self._config.max_task_description_length
        self._validate_detail(detail, max_name, max_desc, "Task")

    def _update_entity_detail(self, entity: Task, detail: Detail) -> None:
        entity.detail = detail
