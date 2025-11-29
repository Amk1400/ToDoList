from typing import List, Type
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import psycopg2
from models.models import Project, Task, Detail
from db.db_interface import DatabaseInterface
from db.orm_models import Base, ProjectORM, TaskORM

class PostgresDatabase(DatabaseInterface):
    """PostgreSQL database using SQLAlchemy ORM with auto-create database."""

    def __init__(
        self,
        db_name: str,
        user: str,
        password: str,
        host: str = "localhost",
        port: int = 5432
    ) -> None:
        self._db_name = db_name
        self._user = user
        self._password = password
        self._host = host
        self._port = port

        # اطمینان از وجود دیتابیس
        self._ensure_database_exists()

        # اتصال اصلی به دیتابیس هدف
        self._engine = create_engine(
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
        )
        self._SessionLocal = sessionmaker(bind=self._engine)

        # ایجاد جدول‌ها در دیتابیس
        Base.metadata.create_all(self._engine)

        # بارگذاری داده‌ها به حافظه
        self.projects: List[Project] = []
        self._load_data()

    # ---------- Database & Table Setup ----------

    def _ensure_database_exists(self) -> None:
        """Create database if it does not exist."""
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port,
            )
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (self._db_name,))
            if not cur.fetchone():
                cur.execute(f'CREATE DATABASE "{self._db_name}"')
                print(f"Database '{self._db_name}' created.")
            else:
                print(f"Database '{self._db_name}' already exists.")
            cur.close()
            conn.close()
        except Exception as e:
            raise RuntimeError(f"Failed to ensure database exists: {e}")

    # ---------- Data Loading ----------

    def _load_data(self) -> None:
        """Load projects and tasks from database into memory."""
        self.projects.clear()
        with self._SessionLocal() as session:
            orm_projects: List[Type[ProjectORM]] = session.query(ProjectORM).all()
            for p in orm_projects:
                tasks = [
                    Task(
                        detail=Detail(title=t.title, description=t.description),
                        deadline=t.deadline,
                        status=t.status
                    )
                    for t in p.tasks
                ]
                project_obj = Project(
                    detail=Detail(title=p.title, description=p.description),
                    tasks=tasks
                )
                self.projects.append(project_obj)
        print(f"Loaded {len(self.projects)} projects from database.")

    def _get_project_orm(self, session: Session, project: Project) -> Type[ProjectORM]:
        orm_project = session.query(ProjectORM).filter_by(title=project.detail.title).first()
        if not orm_project:
            raise ValueError(f"Project '{project.detail.title}' not found in DB.")
        return orm_project

    # ---------- Project Methods ----------

    def add_project(self, project: Project) -> None:
        with self._SessionLocal() as session:
            orm_project = ProjectORM(title=project.detail.title, description=project.detail.description)
            session.add(orm_project)
            session.commit()
            self.projects.append(project)

    def remove_project(self, project: Project) -> None:
        with self._SessionLocal() as session:
            orm_project = self._get_project_orm(session, project)
            session.delete(orm_project)
            session.commit()
            self.projects = [p for p in self.projects if p.detail.title != project.detail.title]

    def get_projects(self) -> List[Project]:
        return self.projects

    # ---------- Task Methods ----------

    def add_task(self, project: Project, task: Task) -> None:
        with self._SessionLocal() as session:
            orm_project = self._get_project_orm(session, project)
            orm_task = TaskORM(
                project_id=orm_project.id,
                title=task.detail.title,
                description=task.detail.description,
                deadline=task.deadline,
                status=task.status
            )
            session.add(orm_task)
            session.commit()
            # update in-memory
            project_obj = next(p for p in self.projects if p.detail.title == project.detail.title)
            project_obj.tasks.append(task)

    def remove_task(self, project: Project, task: Task) -> None:
        with self._SessionLocal() as session:
            orm_project = self._get_project_orm(session, project)
            orm_task = session.query(TaskORM).filter_by(project_id=orm_project.id, title=task.detail.title).first()
            if orm_task:
                session.delete(orm_task)
                session.commit()
            project_obj = next(p for p in self.projects if p.detail.title == project.detail.title)
            project_obj.tasks = [t for t in project_obj.tasks if t.detail.title != task.detail.title]

    def get_tasks(self, project: Project) -> List[Task]:
        proj = next(p for p in self.projects if p.detail.title == project.detail.title)
        return proj.tasks
