from abc import ABC, abstractmethod
from typing import List
from models.models import Detail, Entity, Task, Project


class EntityGateway(ABC):
    """Abstract gateway for fetching entity data from CLI to Service."""

    def __init__(self, manager) -> None:
        """Accept manager instance as input."""
        self._manager = manager

    def get_entities(self)  -> List[Project | Task] | None:
        return self._manager.get_entities()

    def fetch_title(self) -> str:
        """Fetch title from user input; retry until valid according to service."""
        while True:
            title = input("Enter title: ").strip()
            try:
                self._manager.validate_title(title)
                return title
            except ValueError as e:
                print(e)

    def fetch_description(self) -> str:
        """Fetch description from user input; retry until valid according to service."""
        while True:
            description = input("Enter description: ").strip()
            try:
                self._manager.validate_description(description)
                return description
            except ValueError as e:
                print(e)

    def fetch_detail(self) -> Detail:
        """Fetch Detail object by sequentially fetching title and description."""
        title = self.fetch_title()
        description = self.fetch_description()
        return Detail(title=title, description=description)

    def create_entity(self) -> None:
        """Fetch required inputs and apply creation."""
        self._assert_creation_allowed()
        detail = self.fetch_detail()
        optional_args = self._create_fetch_optional()
        self._apply_create(detail, optional_args)

    def _assert_creation_allowed(self) -> None:
        """
        Ensure manager accepts creation before asking user for inputs.

        Raises:
            OverflowError: Entity cannot be created due to limit.
        """
        try:
            self._manager.assert_can_create()
        except OverflowError as exc:
            print(f"❌ Cannot create entity: {exc}")
            raise

    @abstractmethod
    def _create_fetch_optional(self) -> dict:
        """Fetch optional fields during creation; override in child classes."""
        return {}

    def edit_entity(self, entity: object) -> None:
        """Fetch all required inputs and apply edition through service."""
        detail = self.fetch_detail()
        optional_args = self.edit_fetch_optional(entity)
        self._apply_edit(entity, detail, optional_args)

    @abstractmethod
    def delete_entity(self, entity: Entity):
        raise NotImplementedError

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