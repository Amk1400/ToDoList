from abc import ABC, abstractmethod
from typing import Optional, List, Union
from cli.menus.base_menu import BaseMenu
from cli.gateway.project_gateway import ProjectGateway
from cli.gateway.task_gateway import TaskGateway
from models.models import Project, Option, Entity

GatewayType = Union[ProjectGateway, TaskGateway]


class EntityShowMenu(BaseMenu, ABC):
    """Abstract base menu to show entities and select one to modify."""

    def __init__(
        self,
        gateway: GatewayType,
        project: Optional[Project] = None,
        parent_menu: Optional[BaseMenu] = None,
        title: str = "Show Entities"
    ) -> None:
        self._gateway: GatewayType = gateway
        self._project: Optional[Project] = project
        super().__init__(title, parent_menu)

    def _setup_core_options(self) -> None:
        items = self._get_items()
        if not items:
            print(f"\nNo {self._get_entity_name()}s created. You can create one in previous menu.")
            return

        for entity in items:
            entity_option = Option(
                title=str(entity),
                action=lambda e=entity: self._open_modify(e)
            )
            self.add_option(entity_option)

    def _get_items(self) -> List[Entity]:
        """Return list of entities from the gateway."""
        return self._gateway.get_entities()

    @abstractmethod
    def _open_modify(self, entity: Entity) -> None:
        """Open the correct modify menu for the entity."""
        pass

    @abstractmethod
    def _get_entity_name(self) -> str:
        """Open the correct modify menu for the entity."""
        pass