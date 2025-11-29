from __future__ import annotations
from typing import List, Optional
import psycopg2
from psycopg2.extensions import connection as PGConnection
from psycopg2.extras import RealDictCursor
from models.models import Project, Task, Detail
from abc import ABC
from db.db_interface import DatabaseInterface


class PostgresDatabase(DatabaseInterface, ABC):
    """PostgreSQL database connector with auto-create and fetch."""

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
        self._conn: Optional[PGConnection] = None
        self.projects: List[Project] = []

        # بررسی و ایجاد دیتابیس
        self._ensure_database_exists()
        # اتصال به دیتابیس
        self._connect()
        # بررسی و ایجاد جدول‌ها
        self._ensure_tables_exist()
        # بارگذاری داده‌ها
        self._load_data()

    # ---------- Database & Table Setup ----------

    def _ensure_database_exists(self) -> None:
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

    def _connect(self) -> None:
        self._conn = psycopg2.connect(
            dbname=self._db_name,
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port,
        )
        self._conn.autocommit = True
        print(f"Connected to database '{self._db_name}'.")

    def _ensure_tables_exist(self) -> None:
        with self._conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS project (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(100) NOT NULL,
                    description TEXT NOT NULL
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS task (
                    id SERIAL PRIMARY KEY,
                    project_id INTEGER REFERENCES project(id) ON DELETE CASCADE,
                    title VARCHAR(100) NOT NULL,
                    description TEXT NOT NULL,
                    deadline DATE,
                    status VARCHAR(20)
                );
                """
            )
        print("Tables ensured in database.")

    # ---------- Data Loading ----------

    def _load_data(self) -> None:
        """Load projects and tasks from database."""
        self.projects.clear()
        with self._conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM project;")
            projects_raw = cur.fetchall()
            for proj in projects_raw:
                cur.execute("SELECT * FROM task WHERE project_id=%s;", (proj["id"],))
                tasks_raw = cur.fetchall()
                tasks: List[Task] = [
                    Task(
                        detail=Detail(title=t["title"], description=t["description"]),
                        deadline=t["deadline"],
                        status=t["status"]
                    )
                    for t in tasks_raw
                ]
                project_obj = Project(
                    detail=Detail(title=proj["title"], description=proj["description"]),
                    tasks=tasks
                )
                self.projects.append(project_obj)
        print(f"Loaded {len(self.projects)} projects from database.")

    # ---------- Project Methods ----------

    def add_project(self, project: Project) -> None:
        with self._conn.cursor() as cur:
            cur.execute(
                "INSERT INTO project (title, description) VALUES (%s, %s) RETURNING id;",
                (project.detail.title, project.detail.description)
            )
        self.projects.append(project)
        print(f"Project '{project.detail.title}' added.")

    def remove_project(self, project: Project) -> None:
        with self._conn.cursor() as cur:
            cur.execute(
                "DELETE FROM project WHERE title=%s;",
                (project.detail.title,)
            )
        self.projects = [p for p in self.projects if p.detail.title != project.detail.title]
        print(f"Project '{project.detail.title}' removed.")

    def get_projects(self) -> List[Project]:
        return self.projects

    # ---------- Task Methods ----------

    def add_task(self, project: Project, task: Task) -> None:
        proj = self._find_project(project)
        with self._conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO task (project_id, title, description, deadline, status)
                SELECT id, %s, %s, %s, %s FROM project WHERE title=%s;
                """,
                (task.detail.title, task.detail.description, task.deadline, task.status, project.detail.title)
            )
        proj.tasks.append(task)
        print(f"Task '{task.detail.title}' added to project '{project.detail.title}'.")

    def remove_task(self, project: Project, task: Task) -> None:
        proj = self._find_project(project)
        with self._conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM task
                WHERE project_id = (SELECT id FROM project WHERE title=%s)
                  AND title=%s;
                """,
                (project.detail.title, task.detail.title)
            )
        proj.tasks = [t for t in proj.tasks if t.detail.title != task.detail.title]
        print(f"Task '{task.detail.title}' removed from project '{project.detail.title}'.")

    def get_tasks(self, project: Project) -> List[Task]:
        proj = self._find_project(project)
        return proj.tasks

    # ---------- Helper Methods ----------

    def _find_project(self, project: Project) -> Project:
        for p in self.projects:
            if p.detail.title == project.detail.title:
                return p
        raise ValueError(f"Project '{project.detail.title}' not found.")
