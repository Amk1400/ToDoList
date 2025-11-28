from abc import ABC, abstractmethod
from datetime import datetime, date
from typing import Optional, List, Any

from exception.exceptions import (
    EmptyValueError,
    MaxLengthError,
    DuplicateValueError,
    InvalidChoiceError,
    InvalidStatusError,
    InvalidDateError, MaxCountError,
)


class BaseValidator(ABC):
    @abstractmethod
    def validate(self, value: Any) -> Any:
        raise NotImplementedError


class NonEmptyTextValidator(BaseValidator):
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
    def __init__(self, max_count: int, current_count: int, field_name: str) -> None:
        self._max_count = max_count
        self._current_count = current_count
        self._field_name = field_name

    def validate(self, value: Any = None) -> None:
        if self._current_count >= self._max_count:
            raise MaxCountError(self._field_name, self._max_count)


class NumberChoiceValidator(BaseValidator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self._min = min_value
        self._max = max_value

    def validate(self, value: int) -> int:
        if value is None or str(value).strip() == "":
            raise EmptyValueError("choice")

        if not isinstance(value, int):
            raise InvalidChoiceError(self._min, self._max)

        if not (self._min <= value <= self._max):
            raise InvalidChoiceError(self._min, self._max)

        return value


class StatusValidator(BaseValidator):
    ALLOWED_STATUSES = {"todo", "doing", "done"}

    def validate(self, value: Optional[str]) -> Optional[str]:
        if not value or not value.strip():
            return None

        normalized = value.strip().lower()

        if normalized not in self.ALLOWED_STATUSES:
            raise InvalidStatusError(list(self.ALLOWED_STATUSES))

        return normalized


class DeadlineValidator(BaseValidator):
    def validate(self, value: Optional[date]) -> Optional[date]:
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