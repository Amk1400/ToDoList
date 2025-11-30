from typing import TypeVar, Generic, Optional, List
from db.db_interface import DatabaseInterface
from db.entities.project_postgres import ProjectPostgres
from db.entities.task_postgres import TaskPostgres
from db.session import DBSession
from models.models import Project, Task, Detail

T = TypeVar("T", Project, Task)

class PostgresDatabase(DatabaseInterface[T], Generic[T]):
    def __init__(self, url: str):
        self._db_session = DBSession(url)
        self._projects: List[Project] = []
        self._project_entity = ProjectPostgres()
        self._task_entity = TaskPostgres()

        # ساخت جداول
        from db.orm_models import Base
        Base.metadata.create_all(self._db_session.engine)

        self._load()

    def add_project(self, project: Project) -> None:
        with self._db_session.get_session() as session:
            self._project_entity.add_entity(project, self._projects, session)

    def remove_project(self, project: Project) -> None:
        with self._db_session.get_session() as session:
            self._project_entity.remove_entity(project, self._projects, session)

    def add_task(self, project: Project, task: Task) -> None:
        proj_model = self._find_project_model(project)
        with self._db_session.get_session() as session:
            self._task_entity.add_entity(task, proj_model.tasks, session, parent=project)

    def remove_task(self, project: Project, task: Task) -> None:
        proj_model = self._find_project_model(project)
        with self._db_session.get_session() as session:
            self._task_entity.remove_entity(task, proj_model.tasks, session, parent=project)

    def update_entity(self, parent_project: Optional[Project], old_entity: T, new_entity: T) -> None:
        with self._db_session.get_session() as session:
            if parent_project is None:
                self._project_entity.update_entity(old_entity, new_entity, self._projects, session)
            else:
                proj_model = self._find_project_model(parent_project)
                self._task_entity.update_entity(old_entity, new_entity, proj_model.tasks, session, parent=parent_project)

    def get_projects(self) -> List[Project]:
        return self._projects

    def get_tasks(self, project: Project) -> List[Task]:
        return self._find_project_model(project).tasks

    def _load(self) -> None:
        from db.orm_models import ProjectORM
        self._projects.clear()
        with self._db_session.get_session() as session:
            for proj_orm in session.query(ProjectORM).all():
                tasks = self._task_entity.load_all(session, parent=proj_orm)
                self._projects.append(Project(
                    detail=Detail(proj_orm.title, proj_orm.description),
                    tasks=tasks
                ))

    def _find_project_model(self, project: Project) -> Project:
        for p in self._projects:
            if p.detail.title == project.detail.title:
                return p
        raise ValueError(f"Project '{project.detail.title}' not found")
