from datetime import date
from typing import Optional, List

from models.models import Status
from core.validator import (
    StatusValidator,
    DeadlineValidator,
    NonEmptyTextValidator,
    MaxCountValidator,
)


class Validators:
    """Centralized validator utilities."""
    """
    Attributes:
        None: No stored attributes.
    """

    @staticmethod
    def validate_status(status: str) -> Status:
        """Validate and convert status string."""
        """
        Args:
            status (str): Raw status string.

        Returns:
            Status: Validated status enum.

        Raises:
            ValueError: If status is invalid.
        """
        validator = StatusValidator()
        return validator.validate(status)

    @staticmethod
    def validate_deadline(deadline: date) -> None:
        """Validate deadline date."""
        """
        Args:
            deadline (date): Deadline date.

        Returns:
            None: No return value.

        Raises:
            ValueError: If deadline is invalid.
        """
        validator = DeadlineValidator()
        validator.validate(deadline)

    @staticmethod
    def validate_title(
        entity_name: str,
        title: str,
        repo_list: List,
        skip_current: Optional[str] = None,
        max_length: int = 100,
    ) -> None:
        """Validate entity title text."""
        """
        Args:
            entity_name (str): Name of entity.
            title (str): Title text.
            repo_list (List): Existing repository list.
            skip_current (Optional[str]): Value to skip during uniqueness check.
            max_length (int): Max allowed length.

        Returns:
            None: No return value.

        Raises:
            ValueError: If title is invalid or duplicated.
        """
        NonEmptyTextValidator(
            max_length=max_length,
            field_name=f"{entity_name} title",
            existing_values=[e.detail.title for e in repo_list],
            skip_current=skip_current,
        ).validate(title)

    @staticmethod
    def validate_description(
        entity_name: str,
        description: str,
        max_length: int,
    ) -> None:
        """Validate entity description text."""
        """
        Args:
            entity_name (str): Name of entity.
            description (str): Description text.
            max_length (int): Max allowed length.

        Returns:
            None: No return value.

        Raises:
            ValueError: If description is invalid.
        """
        NonEmptyTextValidator(
            max_length=max_length,
            field_name=f"{entity_name} description",
        ).validate(description)

    @staticmethod
    def validate_creation(
        entity_name: str,
        current_count: int,
        max_count: int,
    ) -> None:
        """Validate creation limit for an entity."""
        """
        Args:
            entity_name (str): Name of entity.
            current_count (int): Current count.
            max_count (int): Allowed maximum.

        Returns:
            None: No return value.

        Raises:
            ValueError: If creation exceeds limit.
        """
        MaxCountValidator(
            max_count=max_count,
            current_count=current_count,
            field_name=entity_name,
        ).validate()
