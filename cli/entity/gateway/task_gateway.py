from typing import Optional
from datetime import date
from cli.entity.gateway.entity_gateway import EntityGateway
from models.models import Task, Detail


class TaskGateway(EntityGateway):
    """Gateway for fetching task inputs from CLI to Service."""

    def _fetch_deadline(self, entity: Optional[Task] = None) -> date:
        while True:
            raw_deadline = input("Enter task deadline (YYYY-MM-DD): ").strip()
            try:
                deadline = self._manager.parse_deadline(raw_deadline)  # Service parses + validates
                return deadline
            except ValueError as e:
                print(e)

    def _fetch_status(self, entity: Optional[Task] = None) -> str:
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
        deadline = self._fetch_deadline(entity)
        status = self._fetch_status(entity)
        return {"deadline": deadline, "status": status}

    def _apply_create(self, detail: Detail, optional_args: dict) -> None:
        """Create task using service manager."""
        # Expect optional_args to contain 'deadline'
        deadline = optional_args.get("deadline")
        if deadline is None:
            print("Deadline required to create task.")
            return
        # Task must be added to a project (assume manager knows current project)
        project = self._manager.current_project  # you need to set this before calling
        self._manager.add_task(project, detail, deadline)

    def _apply_edit(self, entity: Task, detail: Detail, optional_args: dict) -> None:
        """Edit task using service manager."""
        project = self._manager.current_project  # you need to set current project context
        self._manager.update_task(
            project,
            project.tasks.index(entity),
            detail=detail,
            deadline=optional_args.get("deadline"),
            status=optional_args.get("status")
        )
