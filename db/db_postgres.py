from typing import List, Optional, TypeVar, Type
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from db.orm_models import ProjectORM, TaskORM, Base
from models.models import Project, Task, Detail
from db.db_interface import DatabaseInterface
T = TypeVar("T")


class PostgresDatabase(DatabaseInterface[T]):
    """PostgreSQL ORM database connector."""

    def __init__(self, url: str) -> None:
        self._engine = create_engine(url, echo=False, future=True)
        self._session_factory = sessionmaker(bind=self._engine, expire_on_commit=False, class_=Session)
        self._projects: List[Project] = []
        Base.metadata.create_all(self._engine)
        self._load()

    def add_project(self, project: Project) -> None:
        try:
            with self._session_factory() as session:
                obj = ProjectORM(title=project.detail.title, description=project.detail.description)
                session.add(obj)
                session.commit()
                self._projects.append(project)
        except Exception as exc:
            raise RuntimeError("Failed to add project.") from exc

    def remove_project(self, project: Project) -> None:
        try:
            with self._session_factory() as session:
                obj = self._find_project_orm(session, project)
                session.delete(obj)
                session.commit()
                self._projects = [p for p in self._projects if p.detail.title != project.detail.title]
        except Exception as exc:
            raise RuntimeError("Failed to remove project.") from exc

    def add_task(self, project: Project, task: Task) -> None:
        try:
            with self._session_factory() as session:
                proj_orm = self._find_project_orm(session, project)
                obj = TaskORM(
                    project_id=proj_orm.id,
                    title=task.detail.title,
                    description=task.detail.description,
                    deadline=task.deadline,
                    status=task.status
                )
                session.add(obj)
                session.commit()
                proj = self._find_project_model(project)
                proj.tasks.append(task)
        except Exception as exc:
            raise RuntimeError("Failed to add task.") from exc

    def remove_task(self, project: Project, task: Task) -> None:
        try:
            with self._session_factory() as session:
                proj = self._find_project_model(project)
                task_orm = self._find_task_orm(session, project, task)
                session.delete(task_orm)
                session.commit()
                proj.tasks = [t for t in proj.tasks if t.detail.title != task.detail.title]
        except Exception as exc:
            raise RuntimeError("Failed to remove task.") from exc

    def update_entity(self, parent: Optional[Project], old: T, new: T) -> None:
        try:
            with self._session_factory() as session:
                if isinstance(old, Project) and isinstance(new, Project):
                    obj = self._find_project_orm(session, old)
                    obj.title = new.detail.title
                    obj.description = new.detail.description
                    session.commit()
                    proj = self._find_project_model(old)
                    proj.detail = new.detail
                elif isinstance(old, Task) and isinstance(new, Task):
                    if parent is None:
                        raise ValueError("Parent project required.")
                    obj = self._find_task_orm(session, parent, old)
                    obj.title = new.detail.title
                    obj.description = new.detail.description
                    obj.deadline = new.deadline
                    obj.status = new.status or obj.status
                    session.commit()
                    t = self._find_task_model(parent, old)
                    t.detail = new.detail
                    t.deadline = new.deadline
                    t.status = new.status or t.status
                else:
                    raise TypeError("Invalid entity types.")
        except Exception as exc:
            raise RuntimeError("Failed to update entity.") from exc

    def get_projects(self) -> List[Project]:
        return self._projects

    def get_tasks(self, project: Project) -> List[Task]:
        proj = self._find_project_model(project)
        return proj.tasks

    def _load(self) -> None:
        try:
            self._projects.clear()
            with self._session_factory() as session:
                objs = session.query(ProjectORM).order_by(ProjectORM.id).all()
                for obj in objs:
                    tasks = [
                        Task(
                            detail=Detail(title=t.title, description=t.description),
                            deadline=t.deadline,
                            status=t.status
                        )
                        for t in sorted(obj.tasks, key=lambda x: x.id)
                    ]
                    model = Project(
                        detail=Detail(title=obj.title, description=obj.description),
                        tasks=tasks
                    )
                    self._projects.append(model)
        except Exception as exc:
            raise RuntimeError("Failed to load data.") from exc

    def _find_project_orm(self, session: Session, project: Project) -> Type[ProjectORM]:
        obj = session.query(ProjectORM).filter_by(title=project.detail.title).one_or_none()
        if obj is None:
            raise ValueError("Project not found.")
        return obj

    def _find_task_orm(self, session: Session, project: Project, task: Task) -> Type[TaskORM]:
        proj = self._find_project_orm(session, project)
        obj = session.query(TaskORM).filter_by(project_id=proj.id, title=task.detail.title).one_or_none()
        if obj is None:
            raise ValueError("Task not found.")
        return obj

    def _find_project_model(self, project: Project) -> Project:
        for p in self._projects:
            if p.detail.title == project.detail.title:
                return p
        raise ValueError("Project model not found.")

    def _find_task_model(self, project: Project, task: Task) -> Task:
        proj = self._find_project_model(project)
        for t in proj.tasks:
            if t.detail.title == task.detail.title:
                return t
        raise ValueError("Task model not found.")
