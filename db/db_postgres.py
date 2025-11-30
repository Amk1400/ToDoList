from __future__ import annotations
from typing import List, Optional, TypeVar, Generic, Type
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from db.orm_models import ProjectORM, TaskORM, Base
from models.models import Project, Task, Detail
from db.db_interface import DatabaseInterface

T = TypeVar("T", Project, Task)


class PostgresDatabase(DatabaseInterface[T], Generic[T]):
    """PostgreSQL ORM database connector with unified entity methods."""

    def __init__(self, url: str) -> None:
        self._engine = create_engine(url, echo=False, future=True)
        self._session_factory = sessionmaker(bind=self._engine, expire_on_commit=False, class_=Session)
        self._projects: List[Project] = []
        Base.metadata.create_all(self._engine)
        self._load()

    # ----------------- Unified Add/Remove -----------------
    def add_entity(self, entity: T, parent: Optional[Project] = None) -> None:
        try:
            with self._session_factory() as session:
                self._apply_add_of(session, entity, parent)
        except Exception as exc:
            raise RuntimeError("Failed to add entity.") from exc

    def remove_entity(self, entity: T, parent: Optional[Project] = None) -> None:
        try:
            with self._session_factory() as session:
                self._apply_remove_of(session, entity, parent)
        except Exception as exc:
            raise RuntimeError("Failed to remove entity.") from exc

    # ----------------- Apply Methods -----------------
    def _apply_add_of(self, session: Session, entity: T, parent: Optional[Project]) -> None:
        container, orm_obj = self._initialize_orm_container(entity, parent, session, for_add=True)
        try:
            session.add(orm_obj)
            session.commit()
            container.append(entity)
        except Exception as exc:
            session.rollback()
            raise RuntimeError("Failed to add entity.") from exc

    def _apply_remove_of(self, session: Session, entity: T, parent: Optional[Project]) -> None:
        container, orm_obj = self._initialize_orm_container(entity, parent, session, for_add=False)
        try:
            session.delete(orm_obj)
            session.commit()
            container.remove(entity)
        except Exception as exc:
            session.rollback()
            raise RuntimeError("Failed to remove entity.") from exc

    def _initialize_orm_container(self, entity: T, parent: Optional[Project], session: Session, for_add: bool):
        if parent is None:  # Project
            if for_add:
                orm_obj = ProjectORM(title=entity.detail.title, description=entity.detail.description)
            else:
                orm_obj = self._find_project_orm(session, entity)
            container: List[T] = self._projects
        else:  # Task
            proj_model = self._find_project_model(parent)
            if for_add:
                proj_orm = self._find_project_orm(session, parent)
                orm_obj = self._create_orm_task(entity, proj_orm)
            else:
                orm_obj = self._find_task_orm(session, parent, entity)
            container = proj_model.tasks
        return container, orm_obj

    def _create_orm_task(self, entity: Task, proj_orm: ProjectORM) -> TaskORM:
        return TaskORM(
            project_id=proj_orm.id,
            title=entity.detail.title,
            description=entity.detail.description,
            deadline=entity.deadline,
            status=entity.status,
        )

    # ----------------- Interface Wrappers -----------------
    def add_project(self, project: Project) -> None:
        self.add_entity(project)

    def add_task(self, project: Project, task: Task) -> None:
        self.add_entity(task, parent=project)

    def remove_project(self, project: Project) -> None:
        self.remove_entity(project)

    def remove_task(self, project: Project, task: Task) -> None:
        self.remove_entity(task, parent=project)

    # ----------------- Update Method -----------------
    def update_entity(self, parent_project: Optional[Project], old_entity: T, new_entity: T) -> None:
        try:
            with self._session_factory() as session:
                if parent_project is None and isinstance(old_entity, Project) and isinstance(new_entity, Project):
                    orm_obj = self._find_project_orm(session, old_entity)
                    self._update_detail_of(new_entity, orm_obj)
                    session.commit()
                    self._find_project_model(old_entity).detail = new_entity.detail
                elif parent_project is not None and isinstance(old_entity, Task) and isinstance(new_entity, Task):
                    orm_obj = self._find_task_orm(session, parent_project, old_entity)
                    self._update_detail_of(new_entity, orm_obj)
                    orm_obj.deadline = new_entity.deadline
                    orm_obj.status = new_entity.status
                    session.commit()
                    model_task = self._find_task_model(parent_project, old_entity)
                    model_task.detail = new_entity.detail
                    model_task.deadline = new_entity.deadline
                    model_task.status = new_entity.status
                else:
                    raise TypeError("Invalid entity types for update.")
        except Exception as exc:
            raise RuntimeError("Failed to update entity.") from exc

    def _update_detail_of(self, new_entity, orm_obj):
        orm_obj.title = new_entity.detail.title
        orm_obj.description = new_entity.detail.description

    # ----------------- Get Methods -----------------
    def get_projects(self) -> List[Project]:
        return self._projects

    def get_tasks(self, project: Project) -> List[Task]:
        return self._find_project_model(project).tasks

    # ----------------- Load Data -----------------
    def _load(self) -> None:
        self._projects.clear()
        try:
            with self._session_factory() as session:
                for obj in session.query(ProjectORM).order_by(ProjectORM.id).all():
                    tasks = [
                        Task(
                            detail=Detail(title=t.title, description=t.description),
                            deadline=t.deadline,
                            status=t.status,
                        )
                        for t in sorted(obj.tasks, key=lambda x: x.id)
                    ]
                    project_model = Project(
                        detail=Detail(title=obj.title, description=obj.description),
                        tasks=tasks,
                    )
                    self._projects.append(project_model)
        except Exception as exc:
            raise RuntimeError("Failed to load data.") from exc

    # ----------------- Helper Find Methods -----------------
    def _find_project_orm(self, session: Session, project: Project) -> Type[ProjectORM]:
        obj = session.query(ProjectORM).filter_by(title=project.detail.title).one_or_none()
        if obj is None:
            raise ValueError(f"Project '{project.detail.title}' not found.")
        return obj

    def _find_task_orm(self, session: Session, project: Project, task: Task) -> Type[TaskORM]:
        proj_orm = self._find_project_orm(session, project)
        obj = session.query(TaskORM).filter_by(project_id=proj_orm.id, title=task.detail.title).one_or_none()
        if obj is None:
            raise ValueError(f"Task '{task.detail.title}' not found in project '{project.detail.title}'.")
        return obj

    def _find_project_model(self, project: Project) -> Project:
        for p in self._projects:
            if p.detail.title == project.detail.title:
                return p
        raise ValueError(f"Project model '{project.detail.title}' not found.")

    def _find_task_model(self, project: Project, task: Task) -> Task:
        proj_model = self._find_project_model(project)
        for t in proj_model.tasks:
            if t.detail.title == task.detail.title:
                return t
        raise ValueError(f"Task model '{task.detail.title}' not found in project '{project.detail.title}'")
