"""Task model for the Todo App."""

from dataclasses import dataclass, field
from datetime import datetime

from src.exceptions import ValidationError


@dataclass
class Task:
    """Represents a todo task.

    Attributes:
        id: Unique sequential identifier (auto-generated)
        title: Required task title (1-500 characters)
        description: Optional additional details
        completed: Completion status (default: False)
        created_at: Timestamp when task was created
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate task fields after initialization."""
        self._validate_title(self.title)

    @staticmethod
    def _validate_title(title: str) -> None:
        """Validate the task title.

        Args:
            title: The title to validate

        Raises:
            ValidationError: If title is empty or exceeds 500 characters
        """
        if not title or not title.strip():
            raise ValidationError("Title is required")
        if len(title) > 500:
            raise ValidationError("Title must be 500 characters or less")

    def toggle_complete(self) -> None:
        """Toggle the completion status of the task."""
        self.completed = not self.completed
