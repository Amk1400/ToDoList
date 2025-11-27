from datetime import date
from typing import Callable, Optional, TypeVar, Any
from exceptions.validator import NumberChoiceValidator

T = TypeVar("T")


def _fetch_with_retry(
        prompt: str,
    parser: Callable[[str], T],
    validator: Optional[Callable[[T], None]] = None
) -> T:
    """Generic fetch loop with retry and validation."""
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
    """CLI fetcher using a generic retry mechanism for all fields."""

    def __init__(self, validator: Any) -> None:
        """Accepts a validator (service/manager) for field validation."""
        self._validator = validator

    def fetch_title(self) -> str:
        return _fetch_with_retry(
            prompt="Enter title: ",
            parser=str,
            validator=self._validator.validate_title
        )

    def fetch_description(self) -> str:
        return _fetch_with_retry(
            prompt="Enter description: ",
            parser=str,
            validator=self._validator.validate_description
        )

    def fetch_deadline(self) -> Optional[date]:
        def parse_deadline(raw: str) -> Optional[date]:
            if not raw:
                return None
            y, m, d = map(int, raw.split("-"))
            return date(y, m, d)

        return _fetch_with_retry(
            prompt="Enter deadline (YYYY-MM-DD or empty): ",
            parser=parse_deadline,
            validator=self._validator.validate_deadline
        )

    def fetch_status(self) -> Optional[str]:
        def parse_status(raw: str) -> Optional[str]:
            return raw if raw else None

        return _fetch_with_retry(
            prompt="Enter status (todo/doing/done or empty): ",
            parser=parse_status,
            validator=self._validator.validate_status
        )

    def fetch_numeric_option(self, num_options: int, prompt: str = "Choose an option: ") -> int:
        def validate_choice(val: int) -> None:
            NumberChoiceValidator(choice=str(val), min_value=1, max_value=num_options).validate()
            return None

        return _fetch_with_retry(
            prompt=prompt,
            parser=int,
            validator=validate_choice
        )
