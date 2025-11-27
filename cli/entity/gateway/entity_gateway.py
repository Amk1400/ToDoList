from abc import ABC, abstractmethod
from typing import List, Dict
from models.models import Detail, Entity, Project, Task


class EntityGateway(ABC):
    """Base gateway for CLI-to-service entity communication."""

    def __init__(self, manager) -> None:
        self._manager = manager

    def get_entities(self) -> List[Project | Task]:
        return self._manager.get_entities()

    def _fetch_title(self) -> str:
        while True:
            title = input("Enter title: ").strip()
            try:
                self._manager.validate_title(title)
                return title
            except ValueError as exc:
                print(exc)

    def _fetch_description(self) -> str:
        while True:
            description = input("Enter description: ").strip()
            try:
                self._manager.validate_description(description)
                return description
            except ValueError as exc:
                print(exc)

    def _fetch_detail(self) -> Detail:
        return Detail(
            title=self._fetch_title(),
            description=self._fetch_description(),
        )

    def create_entity(self) -> None:
        self._manager.assert_can_create()
        detail = self._fetch_detail()
        optional = self._fetch_optional_create()
        self._manager.add_entity(detail, optional["deadline"])

    def edit_entity(self, entity: Entity) -> None:
        detail = self._fetch_detail()
        optional = self._fetch_optional_edit(entity)
        self._manager.update_entity_fields(
            entity,
            detail,
            deadline=optional.get("deadline"),
            status=optional.get("status")
        )

    def delete_entity(self, entity: Entity) -> None:
        self._manager.remove_entity_object(entity)

    @abstractmethod
    def _fetch_optional_create(self) -> Dict:
        return {}

    @abstractmethod
    def _fetch_optional_edit(self, entity: Entity) -> Dict:
        return {}