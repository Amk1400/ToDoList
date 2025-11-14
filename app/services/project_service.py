from app.models.models import Project, Detail
from app.services.entity_service import EntityManager
from app.services.task_service import TaskManager
from app.core.config import AppConfig


class ProjectManager(EntityManager[Project]):
    """Manager for project domain rules."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize project manager with task manager."""
        super().__init__(config)
        self._task_manager = TaskManager(config)
        self._config = config

    def _get_limit_count(self) -> int:
        """Return max projects allowed."""
        return self._config.max_projects

    def _get_limits(self) -> tuple[int, int]:
        """Return max title and description length for projects."""
        return self._config.max_project_name_length, self._config.max_project_description_length

    def get_task_manager(self) -> TaskManager:
        """Return the task manager instance."""
        return self._task_manager