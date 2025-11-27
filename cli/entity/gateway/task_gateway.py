from datetime import date
from cli.entity.gateway.entity_gateway import EntityGateway
from models.models import Task, Project
from service.task_manager import TaskManager


class TaskGateway(EntityGateway):
    """CLI gateway for task creation and editing."""

    def __init__(self, manager: TaskManager, project: Project) -> None:
        super().__init__(manager)
        self._project = project
        manager.set_current_project(project)

    def _fetch_deadline(self) -> date:
        while True:
            raw = input("Enter deadline (YYYY-MM-DD): ").strip()
            try:
                y, m, d = map(int, raw.split("-"))
                deadline = date(y, m, d)
                self._manager.validate_deadline(deadline)
                return deadline
            except Exception as exc:
                print(exc)

    def _fetch_status(self) -> str:
        while True:
            status = input("Enter status (todo/doing/done): ").strip()
            try:
                return self._manager.validate_status(status)
            except ValueError as exc:
                print(exc)

    def _fetch_optional_create(self) -> dict:
        return {"deadline": self._fetch_deadline()}

    def _fetch_optional_edit(self, entity: Task) -> dict:
        return {"deadline": self._fetch_deadline(),"status": self._fetch_status()}

    def set_current_project(self, project: Project) -> None:
        self._project = project
        self._manager.set_current_project(project)
