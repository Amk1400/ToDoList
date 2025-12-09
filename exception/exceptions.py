from models.models import Status


class ValidationError(ValueError):
    """Base validation failure."""
    pass


class EmptyValueError(ValidationError):
    """Raised when a required value is empty."""

    def __init__(self, field_name: str) -> None:
        """Initialize empty value error.

        Args:
            field_name (str): Name of the required field.
        """
        message = f"{field_name} cannot be empty."
        super().__init__(message)


class MaxLengthError(ValidationError):
    """Raised when a value exceeds its maximum length."""

    def __init__(self, field_name: str, max_length: int) -> None:
        """Initialize max length violation.

        Args:
            field_name (str): Name of the validated field.
            max_length (int): Maximum allowed length.
        """
        message = f"{field_name} cannot exceed {max_length} characters."
        super().__init__(message)


class DuplicateValueError(ValidationError):
    """Raised when a value must be unique but already exists."""

    def __init__(self, field_name: str) -> None:
        """Initialize duplicate value error.

        Args:
            field_name (str): Name of the duplicated field.
        """
        message = f"{field_name} must be unique."
        super().__init__(message)


class MaxCountError(ValidationError):
    """Raised when creation exceeds the allowed count."""

    def __init__(self, field_name: str, max_length: int) -> None:
        """Initialize max count error.

        Args:
            field_name (str): Name of the entity type.
            max_length (int): Maximum allowed count.
        """
        message = f"can not create more than {max_length} {field_name}s."
        super().__init__(message)


class InvalidChoiceError(ValidationError):
    """Raised when a numeric choice is outside the allowed range."""

    def __init__(self, min_value: int, max_value: int) -> None:
        """Initialize invalid choice error.

        Args:
            min_value (int): Minimum allowed value.
            max_value (int): Maximum allowed value.
        """
        message = f"Choice must be between {min_value} and {max_value}."
        super().__init__(message)


class InvalidStatusError(ValidationError):
    """Raised when a task status value is not accepted."""

    def __init__(self, allowed: list[Status]) -> None:
        """Initialize invalid status error.

        Args:
            allowed (list[Status]): Allowed status values.
        """
        choices = ", ".join(s.value for s in allowed)
        super().__init__(f"Status must be one of: {choices}.")


class InvalidDateError(ValidationError):
    """Raised when a date value or format is invalid."""

    def __init__(self) -> None:
        """Initialize invalid date format error."""
        message = "Deadline format must be YYYY-MM-DD and not before today."
        super().__init__(message)
