from typing import List, Optional, Type
from sqlalchemy.orm import Session

from db.entities.entity_postgres import EntityPostgres
from db.orm_models import ProjectORM, TaskORM
from models.models import Project, Detail, Task


class ProjectPostgres(EntityPostgres[Project]):
    """PostgreSQL persistence handler for Project entities.

    Attributes:
        None
    """

    def _create_orm_object(
        self,
        entity: Project,
        proj_orm: Optional[ProjectORM],
    ) -> ProjectORM:
        """Create a ProjectORM instance from a Project entity.

        Args:
            entity (Project): Domain project entity.
            proj_orm (Optional[ProjectORM]): Existing ORM instance if present.

        Returns:
            ProjectORM: Newly created ORM object.
        """
        return ProjectORM(title=entity.detail.title, description=entity.detail.description)

    def _apply_deadline_and_task_update(
        self,
        new_entity: Task = None,
        task_orm: TaskORM = None,
    ) -> None:
        """Apply task updates and deadlines to the ORM layer.

        Args:
            new_entity (Task): Updated task entity.
            task_orm (TaskORM): Corresponding ORM task object.

        Returns:
            None: No value is returned.
        """
        return None

    def _fetch_orm(
        self,
        entity: Project,
        session: Session,
        parent: Optional[Project],
        parent_orm: Optional[ProjectORM],
    ) -> Type[ProjectORM]:
        """Fetch the ProjectORM instance corresponding to a Project entity.

        Args:
            entity (Project): Domain project entity.
            session (Session): Active database session.
            parent (Optional[Project]): Parent project entity.
            parent_orm (Optional[ProjectORM]): Parent ORM project instance.

        Returns:
            Type[ProjectORM]: Matching ORM project object.

        Raises:
            ValueError: If the project cannot be found in the database.
        """
        orm_obj = session.query(ProjectORM).filter_by(title=entity.detail.title).one_or_none()
        if orm_obj is None:
            raise ValueError(f"Project '{entity.detail.title}' not found")
        return orm_obj

    def _fetch_parent_proj_orm(
        self,
        parent: Optional[Project],
        session: Session,
    ) -> None:
        """Fetch the parent ProjectORM if applicable.

        Args:
            parent (Optional[Project]): Parent project entity.
            session (Session): Active database session.

        Returns:
            None: Parent projects are not persisted.
        """
        return None

    def load_all(self, session: Session) -> List[Project]:
        """Load all projects and their tasks from the database.

        Args:
            session (Session): Active database session.

        Returns:
            List[Project]: List of loaded domain project entities.
        """
        from db.entities.task_postgres import TaskPostgres

        task_loader = TaskPostgres()
        projects: List[Project] = []

        query = session.query(ProjectORM).order_by(ProjectORM.id.asc())
        orm_projects = query.all()

        for orm_proj in orm_projects:
            tasks = task_loader.load_all(session, parent=orm_proj)
            detail = Detail(orm_proj.title, orm_proj.description)

            project = Project(detail=detail, tasks=tasks)
            project._id = orm_proj.id
            projects.append(project)

        return projects
