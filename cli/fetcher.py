from datetime import date
from typing import Callable, Optional, TypeVar, Any

T = TypeVar("T")


def _fetch_with_retry(
    prompt: str,
    parser: Callable[[str], T],
    validator: Optional[Callable[[T], None]] = None,
) -> T:
    """Loop until valid input is provided based on parser and optional validator."""
    while True:
        raw = input(prompt).strip()
        try:
            value = parser(raw)
            if validator:
                validator(value)
            return value
        except Exception as exc:
            print(f"❌ {exc}")


class CliFetcher:
    """CLI fetcher delegating validation to managers, except numeric options."""

    def __init__(self, manager: Any) -> None:
        """
        Initialize fetcher with a manager that provides validate methods.

        Args:
            manager: Any manager (ProjectManager or TaskManager) that has validate methods.
        """
        self._manager = manager

    def fetch_title(self, current_title: Optional[str] = None) -> str:
        """Fetch title and validate via manager, skipping current title if editing."""

        def validator_wrapper(value: str) -> str:
            return self._manager.validate_title(value, skip_current=current_title)

        return _fetch_with_retry(
            prompt="Enter title: ",
            parser=str,
            validator=validator_wrapper,
        )

    def fetch_description(self) -> str:
        """Fetch description and validate via manager."""
        return _fetch_with_retry(
            prompt="Enter description: ",
            parser=str,
            validator=self._manager.validate_description
        )

    def fetch_deadline(self) -> Optional[date]:
        """Fetch deadline and validate via manager."""
        def parse_deadline(raw: str) -> Optional[date]:
            if not raw:
                return None
            y, m, d = map(int, raw.split("-"))
            return date(y, m, d)

        return _fetch_with_retry(
            prompt="Enter deadline (YYYY-MM-DD): ",
            parser=parse_deadline,
            validator=self._manager.validate_deadline
        )

    def fetch_status(self) -> Optional[str]:
        """Fetch status and validate via manager."""
        def parse_status(raw: str) -> Optional[str]:
            return raw if raw else None

        return _fetch_with_retry(
            prompt="Enter status (todo/doing/done or empty): ",
            parser=parse_status,
            validator=self._manager.validate_status
        )

    def fetch_numeric_option(self, num_options: int, prompt: str = "Choose an option: ") -> int:
        """Fetch numeric menu choice using NumberChoiceValidator directly."""
        from core.validator import NumberChoiceValidator  # فقط برای NumericOption

        def parse_int(raw: str) -> int:
            if not raw:
                raise ValueError("Your choice cannot be empty.")
            return int(raw)

        validator = NumberChoiceValidator(min_value=1, max_value=num_options).validate

        return _fetch_with_retry(
            prompt=prompt,
            parser=parse_int,
            validator=validator
        )
