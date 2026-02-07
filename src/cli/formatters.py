"""Output formatters for the Todo App CLI."""

from src.models.task import Task


def format_success(message: str) -> str:
    """Format a success message.

    Args:
        message: The success message to format

    Returns:
        Formatted success string with checkmark
    """
    return f"✓ {message}"


def format_error(message: str) -> str:
    """Format an error message.

    Args:
        message: The error message to format

    Returns:
        Formatted error string with X mark
    """
    return f"✗ Error: {message}"


def format_task(task: Task) -> str:
    """Format a single task for display.

    Args:
        task: The task to format

    Returns:
        Formatted task string with status indicator
    """
    status = "[x]" if task.completed else "[ ]"
    lines = [f"#{task.id} {status} {task.title}"]

    if task.description:
        lines.append(f"      {task.description}")

    return "\n".join(lines)


def format_task_list(tasks: list[Task]) -> str:
    """Format a list of tasks for display.

    Args:
        tasks: List of tasks to format

    Returns:
        Formatted task list with header and summary
    """
    lines = ["=== Your Tasks ===", ""]

    if not tasks:
        lines.append("No tasks found. Add your first task!")
        return "\n".join(lines)

    for task in tasks:
        lines.append(format_task(task))
        lines.append("")

    # Add summary
    completed = sum(1 for t in tasks if t.completed)
    pending = len(tasks) - completed
    lines.append("────────────────────")
    lines.append(
        f"Total: {len(tasks)} tasks ({completed} completed, {pending} pending)"
    )

    return "\n".join(lines)
