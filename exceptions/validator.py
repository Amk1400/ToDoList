from abc import ABC, abstractmethod
from datetime import date, datetime
from dataclasses import dataclass
from typing import Optional

from tomlkit import value

from .raisor import InvalidOptionException


@dataclass
class ValidationResult:
    """Single validation result with proper type."""
    value: object

    def as_int(self):
        return int(self.value)

class BaseValidator(ABC):
    """Base validator."""

    @abstractmethod
    def validate(self) -> ValidationResult:
        raise NotImplementedError


class NumberChoiceValidator(BaseValidator):
    """Validate numeric menu choice."""
    def __init__(self, choice: str, min_value: int, max_value: int) -> None:
        self._choice = choice
        self._min = min_value
        self._max = max_value

    def validate(self) -> ValidationResult:
        if not self._choice.isdigit():
            raise InvalidOptionException("Input must be a number.")
        value = int(self._choice)
        if not (self._min <= value <= self._max):
            raise InvalidOptionException(
                f"Choice must be between {self._min} and {self._max}."
            )
        return ValidationResult(value)


class NonEmptyTextValidator(BaseValidator):
    """Validate non-empty text and max length."""
    def __init__(self, text: str, max_len: Optional[int] = None, field_name: str = "Value") -> None:
        self._text = text
        self._max_len = max_len
        self._field_name = field_name

    def validate(self) -> ValidationResult:
        text = self._text.strip()
        if not text:
            raise InvalidOptionException(f"{self._field_name} cannot be empty.")
        if self._max_len and len(text) > self._max_len:
            raise InvalidOptionException(f"{self._field_name} cannot exceed {self._max_len} characters.")
        return ValidationResult(text)


class StatusValidator(BaseValidator):
    """Validate task status."""
    _allowed = {"todo", "doing", "done"}

    def __init__(self, status: str) -> None:
        self._status = status.strip().lower()

    def validate(self) -> ValidationResult:
        if not self._status:
            return ValidationResult(None)
        if self._status not in self._allowed:
            raise InvalidOptionException("Status must be one of: todo, doing, done.")
        return ValidationResult(self._status)


class DeadlineValidator(BaseValidator):
    """Validate task deadline."""
    def __init__(self, raw: str) -> None:
        self._raw = raw.strip()

    def validate(self) -> ValidationResult:
        if not self._raw:
            return ValidationResult(None)
        try:
            parsed = datetime.strptime(self._raw, "%Y-%m-%d").date()
        except ValueError as error:
            raise InvalidOptionException("Deadline format must be YYYY-MM-DD.") from error
        if parsed < date.today():
            raise InvalidOptionException("Deadline cannot be before today.")
        return ValidationResult(parsed)
