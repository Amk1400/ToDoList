from typing import List
from core.config import AppConfig
from models.models import Detail, Project
from service.base_manager import BaseManager
from service.task_manager import TaskManager


class ProjectManager(BaseManager[Project]):
    """Manager class responsible for handling all project-level operations."""

    def __init__(self, config: AppConfig) -> None:
        super().__init__(config)
        self._projects: List[Project] = []
        self._task_manager: TaskManager = TaskManager(config)

    def create_project(self, detail: Detail) -> None:
        if len(self._projects) >= self._config.max_projects:
            raise OverflowError("Maximum number of projects reached.")
        if any(p.detail.title == detail.title for p in self._projects):
            raise ValueError("Project title must be unique.")
        self._validate(detail)
        self._projects.append(self._create_entity(detail))

    def update_project(self, idx: int, detail: Detail) -> None:
        if not (0 <= idx < len(self._projects)):
            raise IndexError("Invalid project index.")
        self._validate(detail)
        self._update_entity_detail(self._projects[idx], detail)

    def get_project(self, idx: int) -> Project:
        if not (0 <= idx < len(self._projects)):
            raise IndexError("Invalid project index.")
        return self._projects[idx]

    def remove_project(self, idx: int) -> None:
        project = self.get_project(idx)
        self._projects.remove(project)

    def get_entities(self) -> List[Project]:
        return self._projects

    def get_task_manager(self) -> TaskManager:
        return self._task_manager

    def _entity_name(self) -> str:
        return "Project"

    def _create_entity(self, detail: Detail) -> Project:
        return Project(detail=detail)

    def _validate(self, detail: Detail) -> None:
        max_name = self._config.max_project_name_length
        max_desc = self._config.max_project_description_length
        self._validate_detail(detail, max_name, max_desc, "Project")

    def _update_entity_detail(self, entity: Project, detail: Detail) -> None:
        entity.detail = detail

    def assert_can_create(self) -> None:
        """Ensure project count is below limit."""
        if len(self._projects) >= self._config.max_projects:
            raise OverflowError("Maximum project count reached.")