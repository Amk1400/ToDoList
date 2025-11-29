from typing import List, Optional, TypeVar
from datetime import date
from models.models import Project, Task, Detail
from db.db_interface import DatabaseInterface

T = TypeVar("T")


class InMemoryDatabase(DatabaseInterface[T]):
    """In-memory database implementation with CRUD operations."""

    def __init__(self) -> None:
        self.projects: List[Project] = []
        self._initialize_demo_data()

    # ---------- Project Methods ----------

    def add_project(self, project: Project) -> None:
        self.projects.append(project)

    def remove_project(self, project: Project) -> None:
        proj = self._find_project(project)
        self.projects.remove(proj)

    def get_projects(self) -> List[Project]:
        return self.projects

    # ---------- Task Methods ----------

    def add_task(self, project: Project, task: Task) -> None:
        proj = self._find_project(project)
        if any(t.detail.title == task.detail.title for t in proj.tasks):
            raise ValueError(f"Task '{task.detail.title}' already exists in project '{proj.detail.title}'.")
        proj.tasks.append(task)

    def remove_task(self, project: Project, task: Task) -> None:
        proj = self._find_project(project)
        task_obj = self._find_task(proj, task)
        proj.tasks.remove(task_obj)

    def get_tasks(self, project: Project) -> List[Task]:
        proj = self._find_project(project)
        return proj.tasks

    # ---------- Update Method ----------

    def update_entity(self, parent_project: Optional[Project], old_entity: T, new_entity: T) -> None:
        if isinstance(old_entity, Project) and isinstance(new_entity, Project):
            proj_obj = self._find_project(old_entity)
            proj_obj.detail = new_entity.detail
        elif isinstance(old_entity, Task) and isinstance(new_entity, Task):
            if parent_project is None:
                raise ValueError("Parent project must be provided for tasks.")
            proj = self._find_project(parent_project)
            task_obj = self._find_task(proj, old_entity)
            task_obj.detail = new_entity.detail
            task_obj.deadline = new_entity.deadline
            task_obj.status = new_entity.status or task_obj.status
        else:
            raise TypeError("Entity type mismatch.")

    # ---------- Helper Methods ----------

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

    # ---------- Demo Data ----------

    def _initialize_demo_data(self) -> None:
        project1 = Project(
            detail=Detail("Project A", "Demo project A"),
            tasks=[
                Task(detail=Detail("Task A1", "First task of A"), deadline=date(2025, 1, 10), status="todo")
            ],
        )
        project2 = Project(
            detail=Detail("Project B", "Demo project B"),
            tasks=[
                Task(detail=Detail("Task B1", "First task of B"), deadline=date(2025, 2, 15), status="doing"),
                Task(detail=Detail("Task B2", "Second task of B"), deadline=date(2025, 3, 20), status="todo"),
            ],
        )
        self.projects = [project1, project2]
