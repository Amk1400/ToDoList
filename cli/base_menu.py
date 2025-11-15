from abc import ABC, abstractmethod
from typing import Optional, List
from models.models import Option


class BaseMenu(ABC):
    """Abstract base class for all CLI menus."""

    def __init__(self, title: str, parent_menu: Optional["BaseMenu"] = None) -> None:
        """Initialize a menu with a title and optional parent."""
        self._title: str = title
        self._parent_menu: Optional["BaseMenu"] = parent_menu
        self._options: List[Option] = []
        self._setup_options()

    @abstractmethod
    def _setup_options(self) -> None:
        """Setup menu options."""
        raise NotImplementedError

    def add_option(self, option: Option) -> None:
        """Add an Option to the menu."""
        self._options.append(option)

    def _go_back(self) -> None:
        """Go back to parent menu."""
        if self._parent_menu:
            self._parent_menu.run()

    def run(self) -> None:
        """Display the menu and execute selected option."""
        print(f"\n--- {self._title} ---")
        for idx, opt in enumerate(self._options, start=1):
            print(f"{idx}. {opt.title}")

        while True:
            choice = input("Choose an option: ").strip()
            if not choice.isdigit():
                print("Invalid input, try again.")
                continue

            index = int(choice) - 1
            if 0 <= index < len(self._options):
                self._options[index].action()
                break
            else:
                print("Invalid choice, try again.")
