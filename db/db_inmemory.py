from typing import List, Optional, TypeVar
from datetime import date

from models.models import Project, Task, Detail, Status
from db.db_interface import DatabaseInterface

T = TypeVar("T", Project, Task)


def _find_task(project: Project, task: Task) -> Task:
    for t in project.tasks:
        if t.detail.title == task.detail.title:
            return t
    raise ValueError(f"Task '{task.detail.title}' not found in project '{project.detail.title}'.")


class InMemoryDatabase(DatabaseInterface[T]):
    """In-memory database implementation with CRUD operations."""

    def __init__(self) -> None:
        super().__init__()
        self._load()

    # ---------- Unified Add/Remove Methods ----------

    def add_entity(self, entity: T, parent: Optional[Project] = None) -> None:
        if parent is None:  # Project
            self._projects.append(entity)  # No duplicates check here
        else:  # Task
            proj = self._find_project(parent)
            if any(t.detail.title == entity.detail.title for t in proj.tasks):
                raise ValueError(f"Task '{entity.detail.title}' already exists in project '{proj.detail.title}'.")
            proj.tasks.append(entity)

    def remove_entity(self, entity: T, parent: Optional[Project] = None) -> None:
        if parent is None:
            proj = self._find_project(entity)
            self._projects.remove(proj)
        else:
            proj = self._find_project(parent)
            task_obj = _find_task(proj, entity)
            proj.tasks.remove(task_obj)

    # ---------- Interface Wrappers ----------

    def add_project(self, project: Project) -> None:
        self.add_entity(project)

    def add_task(self, project: Project, task: Task) -> None:
        self.add_entity(task, parent=project)

    def remove_project(self, project: Project) -> None:
        self.remove_entity(project)

    def remove_task(self, project: Project, task: Task) -> None:
        self.remove_entity(task, parent=project)

    # ---------- Update Method ----------

    def update_entity(self, old_entity: T, new_entity: T, parent_project: Optional[Project]) -> None:
        if isinstance(old_entity, Project) and isinstance(new_entity, Project):
            proj_obj = self._find_project(old_entity)
            proj_obj.detail = new_entity.detail
        elif isinstance(old_entity, Task) and isinstance(new_entity, Task):
            if parent_project is None:
                raise ValueError("Parent project must be provided for tasks.")
            proj = self._find_project(parent_project)
            task_obj = _find_task(proj, old_entity)
            task_obj.detail = new_entity.detail
            task_obj.deadline = new_entity.deadline
            task_obj.status = new_entity.status or task_obj.status
        else:
            raise TypeError("Entity type mismatch.")

    # ---------- Get Methods ----------

    def get_projects(self) -> List[Project]:
        return self._projects

    def get_tasks(self, project: Project) -> List[Task]:
        proj = self._find_project(project)
        return proj.tasks

    # ---------- Helper Methods ----------

    def _find_project(self, project: Project) -> Project:
        for p in self._projects:
            if p.detail.title == project.detail.title:
                return p
        raise ValueError(f"Project '{project.detail.title}' not found.")

    # ---------- Demo Data ----------

    def _load(self) -> None:
        project1 = Project(
            detail=Detail("Project A", "Demo project A"),
            tasks=[
                Task(detail=Detail("Task A1", "First task of A"), deadline=date(2025, 1, 10), status=Status.TODO)
            ],
        )
        project2 = Project(
            detail=Detail("Project B", "Demo project B"),
            tasks=[
                Task(detail=Detail("Task B1", "First task of B"), deadline=date(2025, 2, 15), status=Status.DOING),
                Task(detail=Detail("Task B2", "Second task of B"), deadline=date(2025, 3, 20), status=Status.DONE),
            ],
        )
        self._projects = [project1, project2]
