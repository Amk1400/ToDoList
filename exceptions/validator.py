# exceptions/validator.py
from .raisor import InvalidOptionException

def validate_choice(choice: str, min_value: int, max_value: int) -> int:
    """Validate that the choice is a number within the allowed range.

    Args:
        choice (str): User input.
        min_value (int): Minimum allowed value (inclusive).
        max_value (int): Maximum allowed value (inclusive).

    Returns:
        int: The valid choice as integer.

    Raises:
        InvalidOptionException: If input is invalid or out of range.
    """
    if not choice.isdigit():
        raise InvalidOptionException("Input must be a number.")
    value = int(choice)
    if not (min_value <= value <= max_value):
        raise InvalidOptionException(f"Choice must be between {min_value} and {max_value}.")
    return value
