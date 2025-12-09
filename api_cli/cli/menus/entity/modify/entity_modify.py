from abc import abstractmethod
from typing import TypeVar, Generic

from api_cli.cli.menus.base_menu import BaseMenu
from api_cli.gateway.entity_gateway import EntityGateway
from models.models import Option

G = TypeVar("G", bound=EntityGateway)

class EntityModifyMenu(BaseMenu, Generic[G]):
    def __init__(self, gateway: G, manager, entity, parent_menu=None):
        self._gateway: G = gateway
        self._manager = manager
        self._entity = entity
        super().__init__("Modify Entity", parent_menu)

    def _edit_entity(self) -> None:
        try:
            self._gateway.edit_entity(self._entity)
            print(f"✅{self._entity.detail.title} Updated successfully.")
        except Exception as e:
            self.handle_exception(e)
        self._go_back()

    def delete_entity(self) -> None:
        try:
            self._gateway.delete_entity(self._entity)
            print(f"✅{self._entity.detail.title} Deleted successfully.")
        except Exception as e:
            self.handle_exception(e)
        self._go_back()

    def _setup_core_options(self) -> None:
        self.add_option(Option("Edit", self._edit_entity))
        self.add_option(Option("Delete", self.delete_entity))
        self._add_show_tasks_option()

    @abstractmethod
    def _add_show_tasks_option(self):
        raise NotImplementedError