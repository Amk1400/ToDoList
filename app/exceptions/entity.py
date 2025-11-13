from abc import ABC
from typing import Type, Union
from app.models.models import Task, Project
from . import AppError

EntityType = Union[Task, Project]


class EntityError(AppError, ABC):
    """Base class for exceptions that detect Task or Project domain."""

    def __init__(self, entity_or_name: EntityType | str) -> None:
        if isinstance(entity_or_name, str):
            if entity_or_name == "Task":
                self.entity: Type[EntityType] = Task
            elif entity_or_name == "Project":
                self.entity: Type[EntityType] = Project
            else:
                raise ValueError(f"Unsupported entity name: {entity_or_name}")
        else:
            self.entity: Type[EntityType] = type(entity_or_name)

    @property
    def domain(self) -> str:
        """Return the domain based on the entity class."""
        if issubclass(self.entity, Task):
            return "Task"
        elif issubclass(self.entity, Project):
            return "Project"
        else:
            raise TypeError(f"Unsupported entity type: {self.entity}")


class AlreadyExistsError(EntityError):
    """Exception raised when an entity already exists."""

    def message(self) -> str:
        """Return the exception message."""
        return f"{self.domain} creation failed: already exists."


class LimitExceededError(EntityError):
    """Exception raised when the maximum allowed entities limit is exceeded."""

    def message(self) -> str:
        """Return the exception message."""
        return f"{self.domain} creation failed: limit exceeded."


class NotFoundError(EntityError):
    """Exception raised when an entity is not found."""

    def message(self) -> str:
        """Return the exception message."""
        return f"{self.domain} not found. You can create one :)"


class ValidationError(EntityError):
    """Exception raised when entity validation fails."""

    def message(self) -> str:
        """Return the exception message."""
        return f"{self.domain} validation failed."


class StatusError(EntityError):
    """Exception raised when an entity has an invalid status."""

    def message(self) -> str:
        """Return the exception message."""
        return f"{self.domain} status is invalid."
