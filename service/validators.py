from datetime import date
from typing import Optional, List

from models.models import Status
from core.validator import StatusValidator, DeadlineValidator, NonEmptyTextValidator, MaxCountValidator

class Validators:
    """Centralized validators for managers."""

    @staticmethod
    def validate_status(status: str) -> Status:
        validator = StatusValidator()
        return validator.validate(status)

    @staticmethod
    def validate_deadline(deadline: date) -> None:
        validator = DeadlineValidator()
        validator.validate(deadline)

    @staticmethod
    def validate_title(entity_name: str, title: str, repo_list: List, skip_current: Optional[str] = None, max_length: int = 100) -> None:
        NonEmptyTextValidator(
            max_length=max_length,
            field_name=f"{entity_name} title",
            existing_values=[e.detail.title for e in repo_list],
            skip_current=skip_current
        ).validate(title)

    @staticmethod
    def validate_description(entity_name: str, description: str, max_length: int) -> None:
        NonEmptyTextValidator(
            max_length=max_length,
            field_name=f"{entity_name} description"
        ).validate(description)

    @staticmethod
    def validate_creation(entity_name: str, current_count: int, max_count: int) -> None:
        MaxCountValidator(
            max_count=max_count,
            current_count=current_count,
            field_name=entity_name
        ).validate()
