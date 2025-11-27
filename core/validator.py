from abc import ABC, abstractmethod
from datetime import datetime, date
from typing import Optional, List, Any


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


class BaseValidator(ABC):
    """Abstract base class for all validators."""

    @abstractmethod
    def validate(self, value: Any) -> Any:
        """Validate the input and return processed value."""
        raise NotImplementedError


class NonEmptyTextValidator(BaseValidator):
    """Validate non-empty string and max length, with optional uniqueness check."""

    def __init__(
        self,
        max_length: Optional[int] = None,
        field_name: str = "Value",
        existing_values: Optional[List[str]] = None,
        skip_current: Optional[str] = None
    ) -> None:
        self._max_length = max_length
        self._field_name = field_name
        self._existing_values = existing_values or []
        self._skip_current = skip_current

    def validate(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValidationError(f"{self._field_name} cannot be empty.")
        if self._max_length and len(value) > self._max_length:
            raise ValidationError(
                f"{self._field_name} cannot exceed {self._max_length} characters."
            )
        if value in self._existing_values and value != self._skip_current:
            raise ValidationError(f"{self._field_name} must be unique.")
        return value


class MaxCountValidator(BaseValidator):
    """Validate that adding a new entity does not exceed max count."""

    def __init__(self, max_count: int, current_count: int, field_name: str) -> None:
        self._max_count = max_count
        self._current_count = current_count
        self._field_name = field_name

    def validate(self, value: Any = None) -> None:
        if self._current_count >= self._max_count:
            raise ValidationError(f"Maximum {self._field_name} count reached.")


class NumberChoiceValidator(BaseValidator):
    """Validate numeric menu choice within a range."""

    def __init__(self, min_value: int, max_value: int) -> None:
        self._min = min_value
        self._max = max_value

    def validate(self, value: int) -> int:
        if value is None or str(value).strip() == "":
            raise ValidationError("Choice cannot be empty.")
        if not isinstance(value, int):
            raise ValidationError("Choice must be an integer.")
        if not (self._min <= value <= self._max):
            raise ValidationError(f"Choice must be between {self._min} and {self._max}.")
        return value


class StatusValidator(BaseValidator):
    """Validate task status."""

    ALLOWED_STATUSES = {"todo", "doing", "done"}

    def validate(self, value: Optional[str]) -> Optional[str]:
        if not value or not value.strip():
            return None
        value = value.strip().lower()
        if value not in self.ALLOWED_STATUSES:
            raise ValidationError(f"Status must be one of: {', '.join(self.ALLOWED_STATUSES)}.")
        return value


class DeadlineValidator(BaseValidator):
    """Validate task deadline."""

    def validate(self, value: Optional[str]) -> Optional[date]:
        if not value or not value.strip():
            return None
        try:
            parsed_date = datetime.strptime(value.strip(), "%Y-%m-%d").date()
        except ValueError as error:
            raise ValidationError("Deadline format must be YYYY-MM-DD.") from error
        if parsed_date < date.today():
            raise ValidationError("Deadline cannot be before today.")
        return parsed_date
