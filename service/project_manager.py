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

    def update_project(self, idx: int, detail: Detail) -> None:
        self._validate_entity_index(idx)
        self._update_entity_detail(self._entity_list[idx], detail)

    def get_task_manager(self) -> TaskManager:
        return self._task_manager

    def _entity_name(self) -> str:
        return "Project"

    def _create_entity_object(self, detail: Detail, deadline: Optional[date] = None) -> Project:
        return Project(detail=detail)

    def _get_max_desc_length(self) -> int:
        return self._config.max_project_description_length

    def _get_max_title_length(self) -> int:
        return self._config.max_project_name_length

    def assert_can_create(self) -> None:
        self._assert_can_append(self._config.max_projects)
