from datetime import date
from typing import Optional
from core.config import AppConfig
from models.models import Detail, Project
from service.base_manager import BaseManager
from service.task_manager import TaskManager

class ProjectManager(BaseManager[Project]):
    """Manager class responsible for handling all project-level operations."""

    def __init__(self, config: AppConfig) -> None:
        super().__init__(config)
        self._task_manager: TaskManager = TaskManager(config)

    def get_task_manager(self) -> TaskManager:
        return self._task_manager

    def _cascade_delete_tasks(self, entity):
        from service.task_manager import TaskManager
        # Cascade delete tasks
        for task in list(entity.tasks):
            self._task_manager.remove_entity_object(task)

    def entity_name(self) -> str:
        return "Project"

    def _create_entity_object(self, detail: Detail, deadline: Optional[date] = None, status: Optional[str] = None) -> Project:
        return Project(detail=detail)

    def _update_deadline_and_status(self, deadline, entity, status):
        return None

    def _get_max_desc_length(self) -> int:
        return self._config.max_project_description_length

    def _get_max_title_length(self) -> int:
        return self._config.max_project_name_length

    def _get_max_count(self) -> int:
        return self._config.max_projects