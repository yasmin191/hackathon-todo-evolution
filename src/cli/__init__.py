"""CLI package - Command-line interface for the Todo App."""

from src.cli.formatters import (
    format_error,
    format_success,
    format_task,
    format_task_list,
)
from src.cli.menu import display_menu, get_user_choice

__all__ = [
    "display_menu",
    "get_user_choice",
    "format_task",
    "format_task_list",
    "format_error",
    "format_success",
]
