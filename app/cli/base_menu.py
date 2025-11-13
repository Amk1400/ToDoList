from abc import ABC, abstractmethod
from typing import Callable, Dict, Optional


class BaseMenu(ABC):
    """Abstract base class for all menus."""

    def __init__(self, title: str, parent_menu: Optional["BaseMenu"] = None) -> None:
        """Initialize a menu with a title and optional parent.

        Args:
            title (str): Menu title.
            parent_menu (Optional[BaseMenu]): Parent menu reference.
        """
        self._title: str = title
        self._parent_menu: Optional["BaseMenu"] = parent_menu
        self._options: Dict[str, Callable[[], None]] = {}
        self._is_running: bool = True

    def add_option(self, key: str, action: Callable[[], None]) -> None:
        """Add an option to the menu.

        Args:
            key (str): Option key.
            action (Callable): Action function.
        """
        self._options[key] = action

    def run(self) -> None:
        """Run the menu loop."""
        self._is_running = True
        while self._is_running:
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

    @abstractmethod
    def _handle_error(self, error: Exception) -> None:
        """Abstract method to force child classes to implement error handling."""
        raise NotImplementedError