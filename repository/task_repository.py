from typing import List, Optional
from models.models import Project, Task
from repository.entity_repository import EntityRepository

class TaskRepository(EntityRepository[Task]):
    """Repository for Task entities inside projects."""

    def get_db_list(self, project: Optional[Project] = None) -> List[Task]:
        if project is None:
            raise ValueError("Project must be provided for tasks.")
        return self._db.get_tasks(project)

    def append_to_db(self, entity: Task, project: Optional[Project] = None) -> None:
        if project is None:
            raise ValueError("Project must be provided for tasks.")
        self._db.add_task(project, entity)

    def remove_from_db(self, entity: Task, project: Optional[Project] = None) -> None:
        if project is None:
            raise ValueError("Project must be provided for tasks.")
        self._db.remove_task(project, entity)
