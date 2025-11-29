from typing import List, Optional, TypeVar
import psycopg2
from psycopg2.extras import RealDictCursor
from models.models import Project, Task, Detail
from db.db_interface import DatabaseInterface

T = TypeVar("T")


class PostgresDatabase(DatabaseInterface[T]):
    """PostgreSQL database connector with CRUD operations."""

    def __init__(self, db_name: str, user: str, password: str, host: str = "localhost", port: int = 5432) -> None:
        self._db_name = db_name
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._conn: Optional[psycopg2.extensions.connection] = None
        self.projects: List[Project] = []

        self._ensure_database_exists()
        self._connect()
        self._ensure_tables_exist()
        self._load_data()

    # ---------- Database & Table Setup ----------

    def _ensure_database_exists(self) -> None:
        conn = psycopg2.connect(dbname="postgres", user=self._user, password=self._password, host=self._host, port=self._port)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (self._db_name,))
        if not cur.fetchone():
            cur.execute(f'CREATE DATABASE "{self._db_name}"')
        cur.close()
        conn.close()

    def _connect(self) -> None:
        self._conn = psycopg2.connect(dbname=self._db_name, user=self._user, password=self._password, host=self._host, port=self._port)
        self._conn.autocommit = True

    def _ensure_tables_exist(self) -> None:
        with self._conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS project (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(100) UNIQUE NOT NULL,
                    description TEXT NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS task (
                    id SERIAL PRIMARY KEY,
                    project_id INTEGER REFERENCES project(id) ON DELETE CASCADE,
                    title VARCHAR(100) UNIQUE NOT NULL,
                    description TEXT NOT NULL,
                    deadline DATE,
                    status VARCHAR(20)
                );
            """)

    # ---------- Data Loading ----------

    def _load_data(self) -> None:
        self.projects.clear()
        with self._conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM project ORDER BY id;")
            projects_raw = cur.fetchall()
            for proj in projects_raw:
                cur.execute("SELECT * FROM task WHERE project_id=%s ORDER BY id;", (proj["id"],))
                tasks_raw = cur.fetchall()
                tasks: List[Task] = [
                    Task(
                        detail=Detail(title=t["title"], description=t["description"]),
                        deadline=t["deadline"],
                        status=t["status"]
                    ) for t in tasks_raw
                ]
                self.projects.append(Project(detail=Detail(title=proj["title"], description=proj["description"]), tasks=tasks))

    # ---------- Project Methods ----------

    def add_project(self, project: Project) -> None:
        with self._conn.cursor() as cur:
            cur.execute("INSERT INTO project (title, description) VALUES (%s, %s) RETURNING id;", (project.detail.title, project.detail.description))
        self.projects.append(project)

    def remove_project(self, project: Project) -> None:
        with self._conn.cursor() as cur:
            cur.execute("DELETE FROM project WHERE title=%s;", (project.detail.title,))
        self.projects = [p for p in self.projects if p.detail.title != project.detail.title]

    # ---------- Task Methods ----------

    def add_task(self, project: Project, task: Task) -> None:
        proj = self._find_project(project)
        with self._conn.cursor() as cur:
            cur.execute("""
                INSERT INTO task (project_id, title, description, deadline, status)
                SELECT id, %s, %s, %s, %s FROM project WHERE title=%s;
            """, (task.detail.title, task.detail.description, task.deadline, task.status, project.detail.title))
        proj.tasks.append(task)

    def remove_task(self, project: Project, task: Task) -> None:
        proj = self._find_project(project)
        with self._conn.cursor() as cur:
            cur.execute("""
                DELETE FROM task
                WHERE project_id = (SELECT id FROM project WHERE title=%s)
                  AND title=%s;
            """, (project.detail.title, task.detail.title))
        proj.tasks = [t for t in proj.tasks if t.detail.title != task.detail.title]

    # ---------- Update Method ----------

    def update_entity(self, parent_project: Optional[Project], old_entity: T, new_entity: T) -> None:
        if isinstance(old_entity, Project) and isinstance(new_entity, Project):
            proj_obj = self._find_project(old_entity)
            with self._conn.cursor() as cur:
                cur.execute("UPDATE project SET title=%s, description=%s WHERE title=%s;",
                            (new_entity.detail.title, new_entity.detail.description, old_entity.detail.title))
            proj_obj.detail = new_entity.detail
        elif isinstance(old_entity, Task) and isinstance(new_entity, Task):
            if parent_project is None:
                raise ValueError("Parent project must be provided for tasks.")
            proj = self._find_project(parent_project)
            task_obj = self._find_task(proj, old_entity)
            with self._conn.cursor() as cur:
                cur.execute("""
                    UPDATE task
                    SET title=%s, description=%s, deadline=%s, status=COALESCE(%s, status)
                    WHERE project_id=(SELECT id FROM project WHERE title=%s) AND title=%s;
                """, (new_entity.detail.title, new_entity.detail.description, new_entity.deadline, new_entity.status, parent_project.detail.title, old_entity.detail.title))
            task_obj.detail = new_entity.detail
            task_obj.deadline = new_entity.deadline
            task_obj.status = new_entity.status or task_obj.status
        else:
            raise TypeError("Entity type mismatch.")

    # ---------- Helper ----------

    def _find_project(self, project: Project) -> Project:
        for p in self.projects:
            if p.detail.title == project.detail.title:
                return p
        raise ValueError(f"Project '{project.detail.title}' not found.")

    def _find_task(self, project: Project, task: Task) -> Task:
        for t in project.tasks:
            if t.detail.title == task.detail.title:
                return t
        raise ValueError(f"Task '{task.detail.title}' not found in project '{project.detail.title}'.")

    def get_projects(self) -> List[Project]:
        return self.projects

    def get_tasks(self, project: Project) -> List[Task]:
        proj = self._find_project(project)
        return proj.tasks
