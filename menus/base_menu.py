from abc import ABC, abstractmethod
from typing import Callable, Dict, Optional


class BaseMenu(ABC):
    """Abstract base class representing a navigable text-based menu."""

    def __init__(self, title: str, parent_menu: Optional["BaseMenu"] = None) -> None:
        """Initialize the base menu.

        Args:
            title (str): Menu title displayed to the user.
            parent_menu (Optional[BaseMenu]): Parent menu for navigation hierarchy.
        """
        self._title: str = title
        self._parent_menu: Optional["BaseMenu"] = parent_menu
        self._options: Dict[str, Callable[[], None]] = {}
        self._is_running: bool = True

    def add_option(self, key: str, action: Callable[[], None]) -> None:
        """Register a new menu option.

        Args:
            key (str): The user input key triggering the action.
            action (Callable[[], None]): The function executed when selected.
        """
        self._options[key] = action

    def run(self) -> None:
        """Run the menu event loop until exit or navigation.

        Continuously displays options and executes actions based on user input.
        """
        self._is_running = True
        while self._is_running:
            print(f"\n--- {self._title} ---")
            for key, action in self._options.items():
                label = action.__doc__.split("\n")[0] if action.__doc__ else "Option"
                print(f"{key}. {label}")
            choice = input("Choose an option: ").strip()
            action = self._options.get(choice)
            if action:
                try:
                    action()
                except Exception as error:
                    print(f"❌ Error executing action: {error}")
            else:
                print("⚠ Invalid choice. Please try again.")

    def _go_back(self) -> None:
        """Return to the previous (parent) menu if available."""
        self._is_running = False
        if self._parent_menu:
            print("\n↩ Returning to previous menu...")
            self._parent_menu.run()
        else:
            print("\n⚠ No previous menu available. Exiting current context.")

    @abstractmethod
    def _setup_options(self) -> None:
        """Define available menu options.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError
