from datetime import date
from cli.entity.gateway.entity_gateway import EntityGateway
from models.models import Task, Detail, Project
from service.task_manager import TaskManager


class TaskGateway(EntityGateway):
    """Gateway for fetching task inputs from CLI to Service."""

    def __init__(self, manager: TaskManager, project: Project) -> None:
        super().__init__(manager)
        self._manager: TaskManager = manager
        self._project: Project = project
        self._manager.set_current_project(project)

    def _fetch_deadline(self) -> dict:
        while True:
            raw_deadline = input("Enter task deadline (YYYY-MM-DD): ").strip()
            try:
                year, month, day = map(int, raw_deadline.split("-"))
                deadline = date(year, month, day)
                self._manager.validate_deadline(deadline)
                return {"deadline": deadline}
            except ValueError as e:
                print(f"Invalid date: {e}")

    def _fetch_status(self) -> str:
        while True:
            status = input("Enter task status (todo/doing/done): ").strip()
            try:
                return self._manager.validate_status(status)
            except ValueError as e:
                print(e)

    def _fetch_deadline_and_status(self, entity: Task) -> dict:
        """Fetch optional task fields (deadline, status) for editing."""
        deadline = self._fetch_deadline()["deadline"]
        status = self._fetch_status()
        return {"deadline": deadline, "status": status}

    def _apply_create(self, detail: Detail, optional_args: dict) -> None:
        """Create task using service manager."""
        deadline = optional_args.get("deadline")
        if deadline is None:
            print("Deadline required to create task.")
            return
        self._manager.add_entity(detail, deadline)

    def _apply_edit(self, entity: Task, detail: Detail, optional_args: dict) -> None:
        """Edit task using service manager."""
        try:
            idx = self._manager._entity_list.index(entity)
        except ValueError:
            print("Task not found.")
            return
        self._manager.update_task(
            idx=idx,
            detail=detail,
            deadline=optional_args.get("deadline"),
            status=optional_args.get("status")
        )

    @property
    def project(self) -> Project:
        return self._project

    def set_current_project(self, project: Project):
        """Set a new current project and update entity_list."""
        self._project = project
        self._manager.set_current_project(project)
