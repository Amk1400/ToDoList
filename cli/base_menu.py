from abc import ABC, abstractmethod
from typing import Optional, List
from models.models import Option
from exceptions.validator import validate_choice
from exceptions.raisor import InvalidOptionException


class BaseMenu(ABC):
    """Abstract base class for all CLI menus."""

    def __init__(self, title: str, parent_menu: Optional["BaseMenu"] = None) -> None:
        self._title: str = title
        self._parent_menu: Optional["BaseMenu"] = parent_menu
        self._options: List[Option] = []
        self._setup_options()

    @abstractmethod
    def _setup_options(self) -> None:
        raise NotImplementedError

    def add_option(self, option: Option) -> None:
        self._options.append(option)

    def _go_back(self) -> None:
        if self._parent_menu:
            self._parent_menu._setup_options()
            self._parent_menu.run()

    def run(self) -> None:
        print(f"\n--- {self._title} ---")
        for idx, opt in enumerate(self._options, start=1):
            print(f"{idx}. {opt.title}")

        while True:
            choice = input("Choose an option: ").strip()
            try:
                index = validate_choice(choice, 1, len(self._options)) - 1
                self._options[index].action()
                break
            except InvalidOptionException as e:
                print(f"❌ {e}")
