from abc import ABC, abstractmethod
from typing import Optional, Callable, List
from api_cli.cli.fetcher import CliFetcher
from models.models import Option


class BaseMenu(ABC):
    """Base menu abstraction using CliFetcher for all inputs."""

    def __init__(self, title: str, parent_menu: Optional["BaseMenu"] = None, fetcher: Optional[CliFetcher] = None) -> None:
        self._title: str = title
        self._parent_menu: Optional["BaseMenu"] = parent_menu
        self._options: List[Option] = []
        self._fetcher: CliFetcher = fetcher or CliFetcher(None)
        self._setup_options()

    def _setup_options(self) -> None:
        self._options = []
        self._setup_core_options()
        self.add_option(Option("Back", self._go_back))

    @abstractmethod
    def _setup_core_options(self) -> None:
        raise NotImplementedError

    def add_option(self, option: Option) -> None:
        self._options.append(option)

    def _go_back(self) -> None:
        if self._parent_menu:
            self._parent_menu._setup_options()
            self._parent_menu.run()

    def run(self) -> None:
        self._print_menu_title()
        self._print_menu_options()
        self._fetch_and_execute_option()

    def _fetch_and_execute_option(self) -> None:
        choice = self._fetcher.fetch_numeric_option(len(self._options))
        self._options[choice - 1].action()

    def _print_menu_title(self) -> None:
        print(f"\n--- {self._title} ---")

    def _print_menu_options(self) -> None:
        for idx, option in enumerate(self._options, start=1):
            print(f"{idx}. {option.title}")

    def handle_exception(self, error: Exception, callback: Optional[Callable[[], None]] = None) -> None:
        """Print error and optionally execute callback."""
        print(f"❌ Error: {error}")
        if callback:
            callback()