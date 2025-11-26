from datetime import date
from cli.entity.gateway.entity_gateway import EntityGateway
from models.models import Task, Detail, Project
from service.task_manager import TaskManager


class TaskGateway(EntityGateway):
    def __init__(self, manager: TaskManager, project: Project) -> None:
        super().__init__(manager)
        self._manager: TaskManager = manager
        self._project: Project = project

    def _fetch_deadline(self) -> date:
        while True:
            raw_deadline = input("Enter task deadline (YYYY-MM-DD): ").strip()
            try:
                deadline = self._manager.parse_deadline(raw_deadline)  # service validates
                return deadline
            except ValueError as e:
                print(e)

    def _fetch_status(self) -> str:
        while True:
            status = input("Enter task status (todo/doing/done): ").strip()
            try:
                self._manager.validate_status(status)
                return status
            except ValueError as e:
                print(e)

    def _create_fetch_optional(self) -> dict:
        """Fetch optional task fields (deadline) for creation."""
        deadline = self._fetch_deadline()
        return {"deadline": deadline}

    def edit_fetch_optional(self, entity: Task) -> dict:
        """Fetch optional task fields (deadline, status) for editing."""
        deadline = self._fetch_deadline()
        status = self._fetch_status()
        return {"deadline": deadline, "status": status}

    def _apply_create(self, detail: Detail, optional_args: dict) -> None:
        """Create task using service manager."""
        deadline = optional_args.get("deadline")
        if deadline is None:
            print("Deadline required to create task.")
            return
        self._manager.add_task(self._project, detail, deadline)

    def _apply_edit(self, entity: Task, detail: Detail, optional_args: dict) -> None:
        """Edit task using service manager."""
        self._manager.update_task(
            self._project,
            self._project.tasks.index(entity),
            detail,
            deadline=optional_args.get("deadline"),
            status=optional_args.get("status")
        )

    def delete_entity(self, task: Task) -> None:
        """Delete task using manager."""
        try:
            idx = self._project.tasks.index(task)
        except ValueError:
            print("Task not found.")
            return
        self._manager.remove_task(self._project, idx)

    def set_current_project(self,project: Project):
        self._manager.set_current_project(project)

    @property
    def project(self):
        return self._project