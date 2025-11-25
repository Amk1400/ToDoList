from abc import ABC, abstractmethod
from typing import Optional, List, Callable
from models.models import Option
from exceptions.validator import NumberChoiceValidator


class BaseMenu(ABC):
    """Base menu abstraction."""

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
            raw_input_str = input("Choose an option: ").strip()
            try:
                validated_result = NumberChoiceValidator(
                    choice=raw_input_str,
                    min_value=1,
                    max_value=len(self._options)
                ).validate()
                validated_index = validated_result.as_int()-1

                self._options[validated_index].action()
                break
            except Exception as error:
                self.handle_exception(error)

    def handle_exception(
        self,
        error: Exception,
        callback: Optional[Callable[[], None]] = None
    ) -> None:
        """Handle error and optionally execute a callback.

        Args:
            error (Exception): Raised exception.
            callback (Callable|None): Optional callback to run after printing.

        Returns:
            None
        """
        print(f"❌ Error: {error}")
        if callback:
            callback()
