"""Custom exceptions for the Todo App."""


class TodoAppError(Exception):
    """Base exception for Todo App errors."""

    pass


class TaskNotFoundError(TodoAppError):
    """Raised when a task with the given ID does not exist."""

    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task not found: #{task_id}")


class ValidationError(TodoAppError):
    """Raised when input validation fails."""

    def __init__(self, message: str):
        super().__init__(message)
