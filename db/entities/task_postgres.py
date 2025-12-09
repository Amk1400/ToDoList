from typing import List, Optional, Type
from sqlalchemy.orm import Session

from models.models import Task, Detail, Project
from db.entities.entity_postgres import EntityPostgres
from db.orm_models import TaskORM, ProjectORM


class TaskPostgres(EntityPostgres[Task]):
    """PostgreSQL task entity handler."""

    def _create_orm_object(self, entity: Task, parent_proj_orm: ProjectORM) -> TaskORM:
        """Create ORM Task model.

        Args:
            entity (Task): Task domain object.
            parent_proj_orm (ProjectORM): ORM project parent.

        Returns:
            TaskORM: Created ORM instance.
        """
        return TaskORM(
            project_id=parent_proj_orm.id,
            title=entity.detail.title,
            description=entity.detail.description,
            deadline=entity.deadline,
            status=entity.status,
            closed_at=entity.closed_at,
        )

    def _apply_deadline_and_task_update(self, new_entity: Task, old_entity_orm: Type[TaskORM]) -> None:
        """Apply task-specific field updates.

        Args:
            new_entity (Task): Updated task data.
            old_entity_orm (TaskORM): ORM object to modify.
        """
        old_entity_orm.deadline = new_entity.deadline
        old_entity_orm.status = new_entity.status
        if new_entity.closed_at is not None:
            old_entity_orm.closed_at = new_entity.closed_at

    def _fetch_parent_proj_orm(self, parent: Project, session: Session) -> Type[ProjectORM]:
        """Fetch project ORM model for task operations.

        Args:
            parent (Project): Parent project.
            session (Session): Active SQLAlchemy session.

        Returns:
            ProjectORM: ORM representation of the project.

        Raises:
            ValueError: If parent project is missing.
        """
        if parent is None:
            raise ValueError("Parent project must be provided for task.")
        proj_orm = session.query(ProjectORM).filter_by(title=parent.detail.title).one()
        return proj_orm

    def _fetch_orm(
        self,
        entity: Task,
        session: Session,
        parent: Project,
        parent_orm: ProjectORM,
    ) -> Type[TaskORM]:
        """Fetch ORM task model.

        Args:
            entity (Task): Domain task object.
            session (Session): Active DB session.
            parent (Project): Parent project.
            parent_orm (ProjectORM): ORM parent project.

        Returns:
            TaskORM: ORM task instance.

        Raises:
            ValueError: If matching task is not found.
        """
        title = entity.detail.title
        task_orm = (
            session.query(TaskORM)
            .filter_by(project_id=parent_orm.id, title=title)
            .one_or_none()
        )
        if not task_orm:
            raise ValueError(
                f"Task '{entity.detail.title}' not found in project '{parent.detail.title}'"
            )
        return task_orm

    def load_all(
        self, session: Session, parent: Optional[Type[ProjectORM]] = None
    ) -> List[Task]:
        """Load all tasks for a given project.

        Args:
            session (Session): SQLAlchemy session.
            parent (Optional[ProjectORM]): ORM project parent.

        Returns:
            List[Task]: Loaded task objects.
        """
        tasks: List[Task] = []
        if parent is None:
            return tasks

        query = session.query(TaskORM).filter_by(project_id=parent.id)
        task_list = query.order_by(TaskORM.id.asc()).all()

        for orm_obj in task_list:
            detail = Detail(orm_obj.title, orm_obj.description)
            task = Task(
                detail=detail,
                deadline=orm_obj.deadline,
                status=orm_obj.status,
                closed_at=orm_obj.closed_at,
            )
            task._id = orm_obj.id
            tasks.append(task)

        return tasks
