"""Task service for managing todo tasks."""

from typing import Optional

from src.exceptions import TaskNotFoundError, ValidationError
from src.models.task import Task


class TaskService:
    """Manages Task CRUD operations with in-memory storage.

    Attributes:
        _tasks: Dictionary storing tasks by ID
        _next_id: Counter for generating unique task IDs
    """

    def __init__(self):
        """Initialize the TaskService with empty storage."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Create a new task.

        Args:
            title: Required task title (1-500 characters)
            description: Optional task description

        Returns:
            The newly created Task

        Raises:
            ValidationError: If title is invalid
        """
        task = Task(
            id=self._next_id,
            title=title.strip(),
            description=description.strip() if description else "",
        )
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Task:
        """Get a task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task with the given ID

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return self._tasks[task_id]

    def list_tasks(self) -> list[Task]:
        """Get all tasks.

        Returns:
            List of all tasks in creation order
        """
        return list(self._tasks.values())

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Task:
        """Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update
            title: New title (None to keep current)
            description: New description (None to keep current)

        Returns:
            The updated Task

        Raises:
            TaskNotFoundError: If no task exists with the given ID
            ValidationError: If new title is invalid
        """
        task = self.get_task(task_id)

        if title is not None:
            title = title.strip()
            if title:  # Only update if non-empty
                Task._validate_title(title)
                task.title = title

        if description is not None:
            task.description = description.strip()

        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task by ID.

        Args:
            task_id: The ID of the task to delete

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        del self._tasks[task_id]

    def toggle_complete(self, task_id: int) -> Task:
        """Toggle a task's completion status.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            The updated Task

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        task = self.get_task(task_id)
        task.toggle_complete()
        return task
