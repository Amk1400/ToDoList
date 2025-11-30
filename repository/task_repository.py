from typing import List, Optional
from models.models import Project, Task
from repository.entity_repository import EntityRepository

class TaskRepository(EntityRepository[Task]):
    """Repository for Task entities inside projects."""

    def get_db_list(self, project: Optional[Project] = None) -> List[Task]:
        """Return all tasks of a project."""
        if project is None:
            raise ValueError("Project must be provided for tasks.")
        return self._db.get_tasks(project)

    def append_to_db(self, entity: Task, project: Optional[Project] = None) -> None:
        """Add a task to a specific project."""
        if project is None:
            raise ValueError("Project must be provided for tasks.")
        self._db.add_task(project, entity)

    def remove_from_db(self, entity: Task, project: Optional[Project] = None) -> None:
        """Remove a task from a specific project."""
        if project is None:
            raise ValueError("Project must be provided for tasks.")
        self._db.remove_task(project, entity)

    def update_entity(self, parent_project: Optional[Project], old_entity: Task, new_entity: Task) -> None:
        """Update a task in a project."""
        if parent_project is None:
            raise ValueError("Parent project must be provided for tasks.")
        self._db.update_entity(parent_project, old_entity, new_entity)
