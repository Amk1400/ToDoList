from typing import List

from core.config import AppConfig
from models.models import Detail, Project
from repository.project_repository import ProjectRepository
from service.entity_manager import EntityManager
from service.task_manager import TaskManager


class ProjectManager(EntityManager[Project]):
    """Manager for project-level operations."""
    """
    Attributes:
        _db: Database handler.
        _task_manager (TaskManager | None): Related task manager.
    """

    def __init__(self, config: AppConfig, db) -> None:
        """Initialize project manager with repository."""
        """
        Args:
            config (AppConfig): Application configuration.
            db: Database session or handler.

        Returns:
            None: No return value.

        Raises:
            Exception: If initialization fails.
        """
        repository = ProjectRepository(db)
        super().__init__(config, repository)
        self._db = db
        self._task_manager: TaskManager | None = None

    def set_task_manager(self, task_manager: TaskManager) -> None:
        """Assign task manager."""
        """
        Args:
            task_manager (TaskManager): Task manager instance.

        Returns:
            None: No return value.

        Raises:
            None
        """
        self._task_manager = task_manager

    def _cascade_delete_tasks(self, entity: Project) -> None:
        """Cascade delete tasks when project is removed."""
        """
        Args:
            entity (Project): Target project.

        Returns:
            None: No return value.

        Raises:
            None
        """
        task_manager = self.get_task_manager(entity)
        if task_manager:
            task_manager.set_parent_project(entity)
            for task in list(entity.tasks):
                task_manager.remove_entity_object(task)

    def entity_name(self) -> str:
        """Return entity name."""
        """
        Args:
            None

        Returns:
            str: Name of entity.

        Raises:
            None
        """
        return "Project"

    def create_entity_object(self, detail: Detail, deadline=None, status=None) -> Project:
        """Create project entity."""
        """
        Args:
            detail (Detail): Entity detail.
            deadline: Unused.
            status: Unused.

        Returns:
            Project: Constructed project entity.

        Raises:
            None
        """
        return Project(detail=detail)

    def _update_deadline_and_status_by_repo(self, deadline, entity, status):
        """No update logic needed for projects."""
        """
        Args:
            deadline: Unused.
            entity (Project): Target project.
            status: Unused.

        Returns:
            None: No return value.

        Raises:
            None
        """
        return None

    def _get_max_desc_length(self) -> int:
        """Return max description length."""
        """
        Args:
            None

        Returns:
            int: Max length.

        Raises:
            None
        """
        return self._config.max_project_description_length

    def _get_max_title_length(self) -> int:
        """Return max title length."""
        """
        Args:
            None

        Returns:
            int: Max allowed title length.

        Raises:
            None
        """
        return self._config.max_project_name_length

    def _get_max_count(self) -> int:
        """Return max number of projects."""
        """
        Args:
            None

        Returns:
            int: Maximum count.

        Raises:
            None
        """
        return self._config.max_projects

    def get_task_manager(self, project: Project) -> TaskManager | None:
        """Retrieve task manager bound to project."""
        """
        Args:
            project (Project): Target project.

        Returns:
            TaskManager | None: Task manager instance.

        Raises:
            None
        """
        if self._task_manager is None:
            from service.task_manager import TaskManager
            task_manager = TaskManager(self._config, self._db, project)
            self.set_task_manager(task_manager)
        self._task_manager.set_parent_project(project)
        return self._task_manager

    def get_repo_list(self) -> List[Project]:
        """Get list of stored projects."""
        """
        Args:
            None

        Returns:
            List[Project]: All projects.

        Raises:
            None
        """
        return self._repository.get_db_list()

    def _remove_from_repository(
        self,
        entity: Project,
        parent_project: Project | None = None,
    ) -> None:
        """Remove project from repository."""
        """
        Args:
            entity (Project): Project to remove.
            parent_project (Project | None): Unused.

        Returns:
            None: No return value.

        Raises:
            None
        """
        self._repository.remove_from_db(entity)

    def remove_entity_object(self, entity: Project) -> None:
        """Remove project and cascade delete tasks."""
        """
        Args:
            entity (Project): Project to remove.

        Returns:
            None: No return value.

        Raises:
            None
        """
        self._cascade_delete_tasks(entity)
        self._remove_from_repository(entity)
