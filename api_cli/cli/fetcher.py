from datetime import date
from typing import Callable, Optional, TypeVar, Any

T = TypeVar("T")


def _fetch_with_retry(
    prompt: str,
    parser: Callable[[str], T],
    validator: Optional[Callable[[T], None]] = None,
) -> T:
    """Request input repeatedly until parsed and validated successfully.

    Args:
        prompt (str): Input prompt shown to user.
        parser (Callable[[str], T]): Function converting raw input to target type.
        validator (Optional[Callable[[T], None]]): Optional validation callable.

    Returns:
        T: Validated and parsed value.

    Raises:
        Exception: If parsing or validation fails.
    """
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
    """CLI input fetcher with delegated validation.

    Attributes:
        _manager (Any): Manager providing validation methods.
    """

    def __init__(self, manager: Any) -> None:
        """Initialize fetcher with a validation-capable manager.

        Args:
            manager (Any): Manager handling validation logic.

        Returns:
            None: No value is returned.
        """
        self._manager = manager

    def fetch_title(self, current_title: Optional[str] = None) -> str:
        """Fetch and validate entity title.

        Args:
            current_title (Optional[str]): Current title to skip during validation.

        Returns:
            str: Validated title.
        """

        def validator_wrapper(value: str) -> None:
            return self._manager.validate_title(value, skip_current=current_title)

        return _fetch_with_retry(
            prompt="Enter title: ",
            parser=str,
            validator=validator_wrapper,
        )

    def fetch_description(self) -> str:
        """Fetch and validate entity description.

        Returns:
            str: Validated description.
        """
        return _fetch_with_retry(
            prompt="Enter description: ",
            parser=str,
            validator=self._manager.validate_description,
        )

    def fetch_deadline(self) -> Optional[date]:
        """Fetch and validate optional deadline date.

        Returns:
            Optional[date]: Validated deadline date.
        """

        def parse_deadline(raw: str) -> Optional[date]:
            if not raw:
                return None
            y, m, d = map(int, raw.split("-"))
            return date(y, m, d)

        return _fetch_with_retry(
            prompt="Enter deadline (YYYY-MM-DD): ",
            parser=parse_deadline,
            validator=self._manager.validate_deadline,
        )

    def fetch_status(self) -> Optional[str]:
        """Fetch and validate optional task status.

        Returns:
            Optional[str]: Validated status string or None.
        """

        def parse_status(raw: str) -> Optional[str]:
            return raw if raw else None

        return _fetch_with_retry(
            prompt="Enter status (todo/doing/done or empty): ",
            parser=parse_status,
            validator=self._manager.validate_status,
        )

    @staticmethod
    def fetch_numeric_option(num_options: int, prompt: str = "Choose an option: ") -> int:
        """Fetch and validate numeric menu selection.

        Args:
            num_options (int): Number of available options.
            prompt (str): Prompt displayed to the user.

        Returns:
            int: Validated numeric option.

        Raises:
            ValueError: If the input is invalid or out of range.
        """
        from core.validator import NumberChoiceValidator

        def parse_int(raw: str) -> int:
            if not raw:
                raise ValueError("Your choice cannot be empty.")
            return int(raw)

        validator = NumberChoiceValidator(min_value=1, max_value=num_options).validate

        return _fetch_with_retry(
            prompt=prompt,
            parser=parse_int,
            validator=validator,
        )
