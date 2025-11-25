from abc import ABC, abstractmethod
from typing import Optional, Union
from models.models import Detail
from service.project_manager import ProjectManager
from service.task_manager import TaskManager


class EntityGateway(ABC):
    """Abstract gateway for fetching entity data from CLI to Service."""

    def __init__(self, manager: Union[ProjectManager, TaskManager]) -> None:
        """
        Initialize gateway with service manager.

        Args:
            manager (Union[ProjectManager, TaskManager]): Service manager instance for validation.
        """
        self._manager = manager

    def fetch_title(self, entity: Optional[object] = None) -> str:
        """Fetch title from user input; retry until valid according to service."""
        while True:
            title = input("Enter title: ").strip()
            try:
                self._manager._validate_title(title)
                return title
            except ValueError as e:
                print(e)

    def fetch_description(self, entity: Optional[object] = None) -> str:
        """Fetch description from user input; retry until valid according to service."""
        while True:
            description = input("Enter description: ").strip()
            try:
                self._manager._validate_description(description)
                return description
            except ValueError as e:
                print(e)

    def fetch_detail(self, entity: Optional[object] = None) -> Detail:
        """Fetch Detail object by sequentially fetching title and description."""
        title = self.fetch_title(entity)
        description = self.fetch_description(entity)
        return Detail(title=title, description=description)

    def create_entity(self) -> None:
        """Fetch all required inputs and apply creation through service."""
        detail = self.fetch_detail()
        optional_args = self._create_fetch_optional()
        self._apply_create(detail, optional_args)

    @abstractmethod
    def _create_fetch_optional(self) -> dict:
        """Fetch optional fields during creation; override in child classes."""
        return {}

    def edit_entity(self, entity: object) -> None:
        """Fetch all required inputs and apply edition through service."""
        detail = self.fetch_detail(entity)
        optional_args = self.edit_fetch_optional(entity)
        self._apply_edit(entity, detail, optional_args)

    @abstractmethod
    def edit_fetch_optional(self, entity: object) -> dict:
        """Fetch optional fields during edition; override in child classes."""
        return {}

    @abstractmethod
    def _apply_create(self, detail: Detail, optional_args: dict) -> None:
        """Apply creation using service; implemented in child classes."""
        pass

    @abstractmethod
    def _apply_edit(self, entity: object, detail: Detail, optional_args: dict) -> None:
        """Apply edition using service; implemented in child classes."""
        pass
