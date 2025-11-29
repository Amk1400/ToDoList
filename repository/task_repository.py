from typing import List

from models.models import Project, Task
from repository.entity_repository import EntityRepository


class TaskRepository(EntityRepository[Task]):
    """Repository for Task entities inside projects."""

    def get_db_list(self, project: Project) -> List[Task]:
        """Return all tasks of a given project.

        Args:
            project (Project): Owner project.

        Returns:
            List[Task]: Tasks in the project.
        """
        return self._db.get_tasks(project)

    def append_to_db(self, project: Project, task: Task) -> None:
        """Add a task to a project.

        Args:
            project (Project): Owner project.
            task (Task): Task to add.
        """
        self._db.add_task(project, task)

    def remove_from_db(self, project: Project, task: Task) -> None:
        """Remove a task from a project.

        Args:
            project (Project): Owner project.
            task (Task): Task to remove.
        """
        self._db.remove_task(project, task)