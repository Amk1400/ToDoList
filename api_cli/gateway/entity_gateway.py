from abc import ABC, abstractmethod
from typing import Dict, List, Generic, TypeVar, Optional
from api_cli.cli.fetcher import CliFetcher
from models.models import Entity, Detail

T = TypeVar("T", bound=Entity)


class EntityGateway(ABC, Generic[T]):
    """Base CLI coordinator for entity operations."""

    def __init__(self, manager) -> None:
        self._manager = manager
        self._fetcher = CliFetcher(manager)

    def get_entities(self) -> List[T]:
        return self._manager.get_repo_list()

    def create_entity(self) -> None:
        self._manager.validate_creation()
        detail = self._fetch_detail()
        optional = self._fetch_optional_create()
        self._manager.add_entity(detail, optional.get("deadline"), optional.get("status"))

    def edit_entity(self, old_entity: T) -> None:
        """Edit entity and push updates to the manager using new entity object."""
        detail = self._fetch_detail(old_entity.detail.title)
        optional = self._fetch_optional_edit(old_entity)
        new_entity = self._manager.create_entity_object(
            detail,
            optional.get("deadline"),
            optional.get("status")
        )
        # Use the new update_entity_object method
        if hasattr(self._manager, "_parent_project"):
            parent_project = getattr(self._manager, "_parent_project", None)
        else:
            parent_project = None
        self._manager.update_entity_object(old_entity, new_entity, parent_project)

    def delete_entity(self, entity: T) -> None:
        self._manager.remove_entity_object(entity)

    def _fetch_detail(self, curret_title: Optional[str] = None) -> Detail:
        return Detail(
            title=self._fetcher.fetch_title(curret_title),
            description=self._fetcher.fetch_description()
        )

    @abstractmethod
    def _fetch_optional_create(self) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def _fetch_optional_edit(self, entity: T) -> Dict:
        raise NotImplementedError
