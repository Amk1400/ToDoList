from abc import ABC, abstractmethod
from typing import Optional, Callable, List

from api_cli.cli.fetcher import CliFetcher
from models.models import Option


class BaseMenu(ABC):
    """Abstract menu controller."""

    def __init__(self, title: str, parent_menu: Optional["BaseMenu"] = None,
                 fetcher: Optional[CliFetcher] = None) -> None:
        """Initialize base menu.

        Args:
            title (str): Menu title.
            parent_menu (Optional[BaseMenu]): Parent menu reference.
            fetcher (Optional[CliFetcher]): CLI input fetcher.
        """
        self._title: str = title
        self._parent_menu: Optional["BaseMenu"] = parent_menu
        self._options: List[Option] = []
        self._fetcher: CliFetcher = fetcher or CliFetcher(None)
        self._setup_options()

    def _setup_options(self) -> None:
        """Initialize menu and core options."""
        self._options = []
        self._setup_core_options()
        self.add_option(Option("Back", self._go_back))

    @abstractmethod
    def _setup_core_options(self) -> None:
        """Define core menu options."""
        raise NotImplementedError

    def add_option(self, option: Option) -> None:
        """Register new option.

        Args:
            option (Option): Option instance.
        """
        self._options.append(option)

    def _go_back(self) -> None:
        """Return to parent menu."""
        if self._parent_menu:
            self._parent_menu._setup_options()
            self._parent_menu.run()

    def run(self) -> None:
        """Execute menu flow."""
        self._print_menu_title()
        self._print_menu_options()
        self._fetch_and_execute_option()

    def _fetch_and_execute_option(self) -> None:
        """Fetch user selection and run related action."""
        choice = self._fetcher.fetch_numeric_option(len(self._options))
        self._options[choice - 1].action()

    def _print_menu_title(self) -> None:
        """Show menu title."""
        print(f"\n--- {self._title} ---")

    def _print_menu_options(self) -> None:
        """Show selectable options."""
        for idx, option in enumerate(self._options, start=1):
            print(f"{idx}. {option.title}")

    @staticmethod
    def handle_exception(error: Exception, callback: Optional[Callable[[], None]] = None) -> None:
        """Handle exception with optional callback.

        Args:
            error (Exception): Exception instance.
            callback (Optional[Callable]): Optional recovery action.
        """
        print(f"❌ Error: {error}")
        if callback:
            callback()
