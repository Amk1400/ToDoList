from typing import List
from app.core.config import AppConfig
from app.models.models import Detail, Project, Status
from app.services.entity_service import EntityManager
from app.services.task_service import TaskManager
from app.exceptions.entity import ValidationError


class ProjectManager(EntityManager[Project]):
    """Manages project-level operations."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize project manager.

        Args:
            config (AppConfig): Configuration for validation and limits.
        """
        super().__init__(config)
        self._projects: List[Project] = []
        self._task_manager: TaskManager = TaskManager(config)

    def _entity_type(self) -> type:
        """Return entity type."""
        return Project

    def get_collection(self, parent=None) -> List[Project]:
        """Return all projects."""
        return self._projects

    def _get_limit(self, parent=None) -> int:
        """Return max project limit."""
        return self._config.max_projects

    def _create_entity(self, detail: Detail) -> Project:
        """Create new project."""
        return Project(detail=detail)

    def _validate(self, detail: Detail) -> None:
        """Validate project detail."""
        try:
            self._validate_detail(
                detail,
                self._config.max_project_name_length,
                self._config.max_project_description_length,
            )
        except Exception as error:
            raise ValidationError("Project") from error

    def _update_entity_detail(self, entity: Project, detail: Detail, status: Status) -> None:
        """Apply updated detail."""
        entity.detail = detail

    def get_task_manager(self) -> TaskManager:
        """Return task manager."""
        return self._task_manager