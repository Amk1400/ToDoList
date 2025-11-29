from typing import List
from core.config import AppConfig
from db.db_inmemory import InMemoryDatabase
from models.models import Detail, Project
from repository.project_repository import ProjectRepository
from service.entity_manager import EntityManager
from service.task_manager import TaskManager


class ProjectManager(EntityManager[Project]):
    """Manager for project-level operations."""

    def __init__(self, config: AppConfig, db: InMemoryDatabase) -> None:
        repository = ProjectRepository(db)
        super().__init__(config, repository)
        self._config = config
        self._db = db
        self._task_manager: TaskManager | None = None

    def set_task_manager(self, task_manager: TaskManager) -> None:
        """Set TaskManager for cascade delete operations."""
        self._task_manager = task_manager

    def _cascade_delete_tasks(self, entity: Project) -> None:
        task_manager = self.get_task_manager(entity)
        if task_manager:
            task_manager.set_current_project(entity)
            for task in list(entity.tasks):
                self.get_task_manager(entity).remove_entity_object(task)
                print(f"{task.detail.title} deleted cascading")

    def entity_name(self) -> str:
        return "Project"

    def _create_entity_object(self, detail: Detail, deadline=None, status=None) -> Project:
        return Project(detail=detail)

    def _update_deadline_and_status_by_repo(self, deadline, entity, status):
        return None

    def _get_max_desc_length(self) -> int:
        return self._config.max_project_description_length

    def _get_max_title_length(self) -> int:
        return self._config.max_project_name_length

    def _get_max_count(self) -> int:
        return self._config.max_projects

    def get_task_manager(self, project: Project) -> TaskManager | None:
        if self._task_manager is None:
            from service.task_manager import TaskManager
            task_manager = TaskManager(self._config, self._db, project)
            self.set_task_manager(task_manager)
        self._task_manager.set_current_project(project)
        return self._task_manager


    def get_repo_list(self) -> List[Project]:
        return self._repository.get_db_list()

    def _append_to_repository(self, entity: Project) -> None:
        """Append entity to repository."""
        self._repository.append_to_db(entity)

    def _remove_from_repository(self, entity: Project) -> None:
        """Remove entity from repository."""
        self._repository.remove_from_db(entity)