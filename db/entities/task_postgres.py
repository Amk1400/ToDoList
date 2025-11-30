from typing import List, Optional
from sqlalchemy.orm import Session
from models.models import Task, Detail, Project
from db.entities.entity_postgres import EntityPostgres
from db.orm_models import TaskORM, ProjectORM


class TaskPostgres(EntityPostgres[Task]):
    """Task entity operations for PostgreSQL."""

    def add_entity(self, entity: Task, container: List[Task], session: Session,
                   parent: Optional[Project] = None) -> None:
        proj_orm = session.query(ProjectORM).filter_by(title=parent.detail.title).one()
        task_orm = TaskORM(
            project_id=proj_orm.id,
            title=entity.detail.title,
            description=entity.detail.description,
            deadline=entity.deadline,
            status=entity.status,
        )
        session.add(task_orm)
        session.commit()
        container.append(entity)

    def remove_entity(self, entity: Task, container: List[Task], session: Session,
                      parent: Optional[Project] = None) -> None:
        proj_orm = session.query(ProjectORM).filter_by(title=parent.detail.title).one()
        task_orm = session.query(TaskORM).filter_by(project_id=proj_orm.id, title=entity.detail.title).one_or_none()
        if task_orm:
            session.delete(task_orm)
            session.commit()
            container.remove(entity)

    def update_entity(self, old_entity: Task, new_entity: Task, container: List[Task], session: Session,
                      parent: Optional[Project] = None) -> None:
        """Update task in DB and container."""
        if parent is None:
            raise ValueError("Parent project must be provided for task update.")
        proj_orm = session.query(ProjectORM).filter_by(title=parent.detail.title).one()
        task_orm = session.query(TaskORM).filter_by(project_id=proj_orm.id, title=old_entity.detail.title).one_or_none()
        if not task_orm:
            raise ValueError(f"Task '{old_entity.detail.title}' not found in project '{parent.detail.title}'")

        task_orm.title = new_entity.detail.title
        task_orm.description = new_entity.detail.description
        task_orm.deadline = new_entity.deadline
        task_orm.status = new_entity.status
        session.commit()

        # Update in-memory container
        for i, t in enumerate(container):
            if t.detail.title == old_entity.detail.title:
                container[i] = new_entity
                break

    def load_all(self, session: Session, parent: Optional[ProjectORM] = None) -> List[Task]:
        tasks: List[Task] = []
        if parent is None:
            return tasks
        for task_orm in session.query(TaskORM).filter_by(project_id=parent.id).all():
            tasks.append(Task(
                detail=Detail(task_orm.title, task_orm.description),
                deadline=task_orm.deadline,
                status=task_orm.status
            ))
        return tasks
