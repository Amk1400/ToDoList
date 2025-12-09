from models.models import Status


class ValidationError(ValueError):
    """Base validation failure."""
    pass


class EmptyValueError(ValidationError):
    """Value was empty."""

    def __init__(self, field_name: str) -> None:
        message = f"{field_name} cannot be empty."
        super().__init__(message)


class MaxLengthError(ValidationError):
    """Value exceeded max length."""

    def __init__(self, field_name: str, max_length: int) -> None:
        message = f"{field_name} cannot exceed {max_length} characters."
        super().__init__(message)


class DuplicateValueError(ValidationError):
    """Value already exists."""

    def __init__(self, field_name: str) -> None:
        message = f"{field_name} must be unique."
        super().__init__(message)


class MaxCountError(ValidationError):
    """max entity creation limit reached."""

    def __init__(self, field_name: str, max_length: int) -> None:
        message = f"can not create more than {max_length} {field_name}s."
        super().__init__(message)

class InvalidChoiceError(ValidationError):
    """Choice was outside allowed range."""

    def __init__(self, min_value: int, max_value: int) -> None:
        message = f"Choice must be between {min_value} and {max_value}."
        super().__init__(message)


class InvalidStatusError(ValidationError):
    """Status is not allowed."""

    def __init__(self, allowed: list[Status]) -> None:
        choices = ", ".join(s.value for s in allowed)
        super().__init__(f"Status must be one of: {choices}.")


class InvalidDateError(ValidationError):
    """Date format or value was invalid."""

    def __init__(self) -> None:
        message = "Deadline format must be YYYY-MM-DD and not before today."
        super().__init__(message)
