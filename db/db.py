from dataclasses import dataclass
from datetime import date
from typing import List

from models.models import Project, Task, Detail


@dataclass
class DataBase:
    """Simple in-memory database."""
    projects: List[Project]

    def __init__(self) -> None:
        self.projects = []
        self._initialize_demo_data()

    # ---------- Project Methods ----------

    def add_project(self, project: Project) -> None:
        self.projects.append(project)

    def remove_project(self, project: Project) -> None:
        db_project = self._find_project(project)
        self.projects.remove(db_project)

    def get_projects(self) -> List[Project]:
        return self.projects

    # ---------- Task Methods ----------

    def add_task(self, project: Project, task: Task) -> None:
        db_project = self._find_project(project)
        if task in db_project.tasks:
            raise ValueError(f"Task '{task.detail.title}' already exists in project '{db_project.detail.title}'.")
        db_project.tasks.append(task)

    def remove_task(self, project: Project, task: Task) -> None:
        db_project = self._find_project(project)
        if task not in db_project.tasks:
            raise ValueError(f"Task '{task.detail.title}' not found in project '{db_project.detail.title}'.")
        db_project.tasks.remove(task)

    def get_tasks(self, project: Project) -> List[Task]:
        db_project = self._find_project(project)
        return db_project.tasks

    # ---------- Helper Methods ----------

    def _find_project(self, project: Project) -> Project:
        for p in self.projects:
            if p.detail.title == project.detail.title:
                return p
        raise ValueError(f"Project '{project.detail.title}' not found.")

    def _initialize_demo_data(self) -> None:
        """Load demo projects."""
        project1 = Project(
            detail=Detail("Project A", "Demo project A"),
            tasks=[
                Task(
                    detail=Detail("Task A1", "First task of A"),
                    deadline=date(2025, 1, 10),
                    status="todo",
                )
            ],
        )

        project2 = Project(
            detail=Detail("Project B", "Demo project B"),
            tasks=[
                Task(
                    detail=Detail("Task B1", "First task of B"),
                    deadline=date(2025, 2, 15),
                    status="doing",
                ),
                Task(
                    detail=Detail("Task B2", "Second task of B"),
                    deadline=date(2025, 3, 20),
                    status="todo",
                ),
            ],
        )

        self.projects = [project1, project2]
