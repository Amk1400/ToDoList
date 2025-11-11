from abc import ABC
from app.models.models import Task, Project
from . import AppError


class EntityError(AppError, ABC):
    """Base class for exceptions that automatically detect Task or Project domain.

    Attributes:
        entity (Task | Project): The entity instance causing the exception.
    """

    def __init__(self, entity: Task | Project) -> None:
        """Initialize the entity-aware error.

        Args:
            entity (Task | Project): The entity that triggered the exception.
        """
        self.entity: Task | Project = entity

    @property
    def domain(self) -> str:
        """Determine the domain based on the entity type.

        Returns:
            str: 'Task' if the entity is a Task, 'Project' if the entity is a Project.

        Raises:
            TypeError: If the entity type is unsupported.
        """
        if isinstance(self.entity, Task):
            return "Task"
        elif isinstance(self.entity, Project):
            return "Project"
        else:
            raise TypeError(f"Unsupported entity type: {type(self.entity).__name__}")


class AlreadyExistsError(EntityError):
    """Exception raised when an entity already exists."""

    def message(self) -> str:
        """Return the exception message.

        Returns:
            str: Message indicating that creation failed because the entity already exists.
        """
        return f"{self.domain} creation failed: already exists."


class LimitExceededError(EntityError):
    """Exception raised when the maximum allowed entities limit is exceeded."""

    def message(self) -> str:
        """Return the exception message.

        Returns:
            str: Message indicating that creation failed due to limit exceeded.
        """
        return f"{self.domain} creation failed: limit exceeded."


class NotFoundError(EntityError):
    """Exception raised when an entity is not found."""

    def message(self) -> str:
        """Return the exception message.

        Returns:
            str: Message indicating that the entity was not found.
        """
        return f"{self.domain} not found."


class ValidationError(EntityError):
    """Exception raised when entity validation fails."""

    def message(self) -> str:
        """Return the exception message.

        Returns:
            str: Message indicating that validation failed for the entity.
        """
        return f"{self.domain} validation failed."


class StatusError(EntityError):
    """Exception raised when an entity has an invalid status."""

    def message(self) -> str:
        """Return the exception message.

        Returns:
            str: Message indicating that the entity's status is invalid.
        """
        return f"{self.domain} status is invalid."
