from abc import ABC, abstractmethod
from typing import Dict, List, Generic, TypeVar, Optional

from api_cli.cli.fetcher import CliFetcher
from models.models import Entity, Detail

T = TypeVar("T", bound=Entity)


class EntityGateway(ABC, Generic[T]):
    """Base CLI coordinator for entity operations.

    Attributes:
        _manager (Any): Service-layer manager handling entity logic.
        _fetcher (CliFetcher): CLI input fetcher instance.
    """

    def __init__(self, manager) -> None:
        """Initialize the entity gateway with a manager.

        Args:
            manager (Any): Entity manager service.

        Returns:
            None: No value is returned.
        """
        self._manager = manager
        self._fetcher = CliFetcher(manager)

    def get_entities(self) -> List[T]:
        """Retrieve all managed entities.

        Returns:
            List[T]: List of domain entities.
        """
        return self._manager.get_repo_list()

    def create_entity(self) -> None:
        """Create a new entity using CLI input.

        Returns:
            None: No value is returned.

        Raises:
            Exception: If validation or creation fails.
        """
        self._manager.validate_creation()
        detail = self._fetch_detail()
        optional = self._fetch_optional_create()
        self._manager.add_entity(
            detail,
            optional.get("deadline"),
            optional.get("status"),
        )

    def edit_entity(self, old_entity: T) -> None:
        """Edit an existing entity using CLI input.

        Args:
            old_entity (T): Existing domain entity.

        Returns:
            None: No value is returned.

        Raises:
            Exception: If update fails.
        """
        detail = self._fetch_detail(old_entity.detail.title)
        optional = self._fetch_optional_edit(old_entity)
        new_entity = self._manager.create_entity_object(
            detail,
            optional.get("deadline"),
            optional.get("status"),
        )
        if hasattr(self._manager, "_parent_project"):
            parent_project = getattr(self._manager, "_parent_project", None)
        else:
            parent_project = None
        self._manager.update_entity_object(old_entity, new_entity, parent_project)

    def delete_entity(self, entity: T) -> None:
        """Delete an entity using the manager.

        Args:
            entity (T): Target domain entity.

        Returns:
            None: No value is returned.
        """
        self._manager.remove_entity_object(entity)

    def _fetch_detail(self, current_title: Optional[str] = None) -> Detail:
        """Fetch entity detail fields from CLI.

        Args:
            current_title (Optional[str]): Existing title to prefill input.

        Returns:
            Detail: Constructed detail value object.
        """
        return Detail(
            title=self._fetcher.fetch_title(current_title),
            description=self._fetcher.fetch_description(),
        )

    @abstractmethod
    def _fetch_optional_create(self) -> Dict:
        """Fetch optional fields during entity creation.

        Returns:
            Dict: Optional creation fields.
        """
        raise NotImplementedError

    @abstractmethod
    def _fetch_optional_edit(self, entity: T) -> Dict:
        """Fetch optional fields during entity editing.

        Args:
            entity (T): Target domain entity.

        Returns:
            Dict: Optional edit fields.
        """
        raise NotImplementedError
