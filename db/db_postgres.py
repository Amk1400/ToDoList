from typing import TypeVar, Optional, List

from db.db_interface import DatabaseInterface
from db.entities.project_postgres import ProjectPostgres
from db.entities.task_postgres import TaskPostgres
from db.session import DBSession
from models.models import Project, Task

T = TypeVar("T", Project, Task)


class PostgresDatabase(DatabaseInterface[T]):
    """PostgreSQL-backed database handler."""

    def __init__(self, url: str, use_alembic: bool = False) -> None:
        """Initialize PostgreSQL database interface.

        Args:
            url (str): Connection URL for PostgreSQL.
            use_alembic (bool): Whether Alembic handles migrations.

        Raises:
            RuntimeError: If database initialization fails.
        """
        super().__init__()
        self._project_entity = ProjectPostgres()
        self._task_entity = TaskPostgres()
        self._db_session = DBSession(url, use_alembic=use_alembic)

        if not use_alembic:
            from db.orm_models import Base
            Base.metadata.create_all(self._db_session.engine)

        self._load()

    def add_project(self, project: Project) -> None:
        """Store a new project.

        Args:
            project (Project): Project instance to persist.
        """
        with self._db_session.get_session() as session:
            self._project_entity.add_entity(project, self._projects, session)

    def remove_project(self, project: Project) -> None:
        """Remove an existing project.

        Args:
            project (Project): Project instance to delete.
        """
        with self._db_session.get_session() as session:
            self._project_entity.remove_entity(project, self._projects, session)

    def add_task(self, parent_project: Project, task: Task) -> None:
        """Add a task to a specific project.

        Args:
            parent_project (Project): Associated parent project.
            task (Task): Task instance to persist.
        """
        proj_model = self._find_project_model(parent_project)
        with self._db_session.get_session() as session:
            self._task_entity.add_entity(task, proj_model.tasks, session, parent=parent_project)

    def remove_task(self, parent_project: Project, task: Task) -> None:
        """Remove a task from a project.

        Args:
            parent_project (Project): Parent project of the task.
            task (Task): Task instance to remove.
        """
        proj_model = self._find_project_model(parent_project)
        with self._db_session.get_session() as session:
            self._task_entity.remove_entity(task, proj_model.tasks, session, parent=parent_project)

    def update_entity(self, old_entity: T, new_entity: T, parent_project: Optional[Project]) -> None:
        """Update a stored project or task.

        Args:
            old_entity (T): Existing entity to update.
            new_entity (T): Updated entity.
            parent_project (Optional[Project]): Project context for tasks.

        Raises:
            ValueError: If expected project is not found.
        """
        with self._db_session.get_session() as session:
            if parent_project is None:
                self._project_entity.update_entity(old_entity, new_entity, self._projects, session)
            else:
                proj_model = self._find_project_model(parent_project)
                self._task_entity.update_entity(
                    old_entity, new_entity, proj_model.tasks, session, parent=parent_project
                )

    def get_projects(self) -> List[Project]:
        """Return all stored projects.

        Returns:
            List[Project]: List of persisted projects.
        """
        return self._projects

    def get_tasks(self, project: Project) -> List[Task]:
        """Return tasks belonging to a project.

        Args:
            project (Project): Target project.

        Returns:
            List[Task]: List of tasks for the project.
        """
        return self._find_project_model(project).tasks

    def _load(self) -> None:
        """Load and cache all project data."""
        self._projects.clear()
        with self._db_session.get_session() as session:
            loaded = self._project_entity.load_all(session)
            loaded.sort(key=lambda p: p.id)
            self._projects.extend(loaded)

    def _find_project_model(self, project: Project) -> Project:
        """Find matching project model by title.

        Args:
            project (Project): Target project.

        Returns:
            Project: Matching project model.

        Raises:
            ValueError: When project cannot be found.
        """
        for p in self._projects:
            if p.detail.title == project.detail.title:
                return p
        raise ValueError(f"Project '{project.detail.title}' not found")
