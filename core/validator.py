from abc import ABC, abstractmethod
from datetime import datetime, date
from typing import Optional, List, Any

from exception.exceptions import (
    EmptyValueError,
    MaxLengthError,
    DuplicateValueError,
    InvalidChoiceError,
    InvalidStatusError,
    InvalidDateError,
    MaxCountError,
)
from models.models import Status


class BaseValidator(ABC):
    """Abstract base class for value validators.

    Attributes:
        None
    """

    @abstractmethod
    def validate(self, value: Any) -> Any:
        """Validate a given value.

        Args:
            value (Any): Value to validate.

        Returns:
            Any: Validated value.

        Raises:
            Exception: If validation fails.
        """
        raise NotImplementedError


class NonEmptyTextValidator(BaseValidator):
    """Validator for non-empty unique text fields.

    Attributes:
        _max_length (Optional[int]): Maximum allowed length.
        _field_name (str): Field name for error messages.
        _existing_values (List[str]): Already existing values.
        _skip_current (Optional[str]): Value to skip during duplication check.
    """

    def __init__(
        self,
        max_length: Optional[int] = None,
        field_name: str = "Value",
        existing_values: Optional[List[str]] = None,
        skip_current: Optional[str] = None,
    ) -> None:
        self._max_length = max_length
        self._field_name = field_name
        self._existing_values = existing_values or []
        self._skip_current = skip_current

    def validate(self, value: str) -> str:
        """Validate non-empty text and enforce constraints.

        Args:
            value (str): Text value to validate.

        Returns:
            str: Cleaned and validated text.

        Raises:
            EmptyValueError: If the value is empty.
            MaxLengthError: If the value exceeds max length.
            DuplicateValueError: If the value already exists.
        """
        value = value.strip()

        if not value:
            raise EmptyValueError(self._field_name)

        if self._max_length and len(value) > self._max_length:
            raise MaxLengthError(self._field_name, self._max_length)

        if (
            value in self._existing_values
            and (self._skip_current is None or value != self._skip_current)
        ):
            raise DuplicateValueError(self._field_name)

        return value


class MaxCountValidator(BaseValidator):
    """Validator enforcing a maximum count limit.

    Attributes:
        _max_count (int): Maximum allowed count.
        _current_count (int): Current existing count.
        _field_name (str): Field name for error messages.
    """

    def __init__(self, max_count: int, current_count: int, field_name: str) -> None:
        self._max_count = max_count
        self._current_count = current_count
        self._field_name = field_name

    def validate(self, value: Any = None) -> None:
        """Validate that the maximum count has not been exceeded.

        Args:
            value (Any): Ignored value placeholder.

        Returns:
            None: No value is returned.

        Raises:
            MaxCountError: If the maximum count is exceeded.
        """
        if self._current_count >= self._max_count:
            raise MaxCountError(self._field_name, self._max_count)


class NumberChoiceValidator(BaseValidator):
    """Validator for bounded integer choices.

    Attributes:
        _min (int): Minimum valid value.
        _max (int): Maximum valid value.
    """

    def __init__(self, min_value: int, max_value: int) -> None:
        self._min = min_value
        self._max = max_value

    def validate(self, value: int) -> None:
        """Validate an integer choice within bounds.

        Args:
            value (int): Selected integer value.

        Returns:
            None: No value is returned.

        Raises:
            EmptyValueError: If the value is empty.
            InvalidChoiceError: If the value is invalid or out of range.
        """
        if value is None or str(value).strip() == "":
            raise EmptyValueError("choice")

        if not isinstance(value, int):
            raise InvalidChoiceError(self._min, self._max)

        if not (self._min <= value <= self._max):
            raise InvalidChoiceError(self._min, self._max)


class StatusValidator(BaseValidator):
    """Validator for task status values.

    Attributes:
        ALLOWED_STATUSES (List[Status]): Permitted status values.
    """

    ALLOWED_STATUSES = [Status.TODO, Status.DOING, Status.DONE]

    def validate(self, value: Optional[str]) -> Optional[Status]:
        """Validate and parse a status value.

        Args:
            value (Optional[str]): Raw status input.

        Returns:
            Optional[Status]: Parsed status or None.

        Raises:
            InvalidStatusError: If the status is invalid.
        """
        if value is None or not value.strip():
            return None

        raw = value.strip().lower()

        try:
            status = Status(raw)
        except ValueError:
            raise InvalidStatusError(self.ALLOWED_STATUSES)

        return status


class DeadlineValidator(BaseValidator):
    """Validator for future deadline dates.

    Attributes:
        None
    """

    def validate(self, value: Optional[date]) -> Optional[date]:
        """Validate a deadline date value.

        Args:
            value (Optional[date]): Deadline date or string.

        Returns:
            Optional[date]: Validated deadline date.

        Raises:
            InvalidDateError: If the date is invalid or in the past.
        """
        if value is None:
            return None
        if isinstance(value, str):
            try:
                value = datetime.strptime(value.strip(), "%Y-%m-%d").date()
            except ValueError as error:
                raise InvalidDateError() from error
        if value < date.today():
            raise InvalidDateError()
        return value
