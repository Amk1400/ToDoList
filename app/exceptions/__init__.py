from abc import ABC, abstractmethod


class AppError(Exception, ABC):
    """Base class for all application-specific exceptions."""

    @abstractmethod
    def message(self) -> str:
        """Return the exception message.

        Returns:
            str: Exception message.
        """
        pass

    def __str__(self) -> str:
        """Return string representation of the exception.

        Returns:
            str: The exception message.
        """
        return self.message()
