from abc import ABC, abstractmethod
from typing import Dict, List, Generic, TypeVar
from cli.fetcher import CliFetcher
from models.models import Entity, Detail

T = TypeVar("T", bound=Entity)


class EntityGateway(ABC, Generic[T]):
    """Base CLI coordinator for entity operations."""

    def __init__(self, manager) -> None:
        self._manager = manager
        self._fetcher = CliFetcher(manager)

    def get_entities(self) -> List[T]:
        return self._manager.get_entities()

    def create_entity(self) -> None:
        self._manager.assert_can_create()
        detail = self._fetch_detail()
        optional = self._fetch_optional_create()
        self._manager.add_entity(detail, optional.get("deadline"))

    def edit_entity(self, entity: T) -> None:
        detail = self._fetch_detail()
        optional = self._fetch_optional_edit(entity)
        self._manager.update_entity_fields(entity, detail, **optional)

    def delete_entity(self, entity: T) -> None:
        self._manager.remove_entity_object(entity)

    def _fetch_detail(self) -> Detail:
        return Detail(title=self._fetcher.fetch_title(),description=self._fetcher.fetch_description())

    @abstractmethod
    def _fetch_optional_create(self) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def _fetch_optional_edit(self, entity: T) -> Dict:
        raise NotImplementedError