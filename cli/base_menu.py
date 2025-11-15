from abc import ABC, abstractmethod
from typing import Callable, Dict, Optional


class BaseMenu(ABC):
    """Abstract base class for all cli."""

    def __init__(self, title: str, parent_menu: Optional["BaseMenu"] = None) -> None:
        """Initialize a menu with a title and optional parent.

        Args:
            title (str): Menu title.
            parent_menu (Optional[BaseMenu]): Parent menu reference.
        """
        self._title: str = title
        self._parent_menu: Optional["BaseMenu"] = parent_menu
        self._options = []#TODO

    def add_option(self):
        ...#TODO



    def run(self) -> None:
        """Run the menu loop."""
        print(f"\n--- {self._title} ---")
        for key, action in self._options.items():
            doc = action.__doc__.split(".")[0] if action.__doc__ else "Option"
            print(f"{key}. {doc}")
        choice = input("Choose an option: ").strip()
        action = self._options.get(choice)
        if action:
            action()
        else:
            print("Invalid choice.")

    def _go_back(self) -> None:
        """Go back to previous menu."""
        self._is_running = False
        if self._parent_menu:
            self._parent_menu.run()

    @abstractmethod
    def _setup_options(self) -> None:
        """Setup menu options."""
        raise NotImplementedError
