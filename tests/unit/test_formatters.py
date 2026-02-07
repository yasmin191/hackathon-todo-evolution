"""Unit tests for the CLI formatters."""

from datetime import datetime

import pytest

from src.cli.formatters import (
    format_error,
    format_success,
    format_task,
    format_task_list,
)
from src.models.task import Task


class TestFormatSuccess:
    """Tests for format_success()."""

    def test_format_success_includes_checkmark(self):
        """Test that success message includes checkmark."""
        result = format_success("Task created")

        assert result == "✓ Task created"

    def test_format_success_with_task_details(self):
        """Test formatting success with task details."""
        result = format_success("Task created: #1 - Buy groceries")

        assert "✓" in result
        assert "#1" in result
        assert "Buy groceries" in result


class TestFormatError:
    """Tests for format_error()."""

    def test_format_error_includes_x_mark(self):
        """Test that error message includes X mark."""
        result = format_error("Title is required")

        assert result == "✗ Error: Title is required"

    def test_format_error_with_task_not_found(self):
        """Test formatting error for task not found."""
        result = format_error("Task not found: #999")

        assert "✗ Error:" in result
        assert "#999" in result


class TestFormatTask:
    """Tests for format_task()."""

    def test_format_pending_task(self):
        """Test formatting a pending task."""
        task = Task(id=1, title="Buy groceries", completed=False)

        result = format_task(task)

        assert "#1" in result
        assert "[ ]" in result
        assert "Buy groceries" in result

    def test_format_completed_task(self):
        """Test formatting a completed task."""
        task = Task(id=2, title="Call mom", completed=True)

        result = format_task(task)

        assert "#2" in result
        assert "[x]" in result
        assert "Call mom" in result

    def test_format_task_with_description(self):
        """Test formatting a task with description."""
        task = Task(id=1, title="Buy groceries", description="Milk, eggs, bread")

        result = format_task(task)

        assert "Buy groceries" in result
        assert "Milk, eggs, bread" in result

    def test_format_task_without_description(self):
        """Test formatting a task without description."""
        task = Task(id=1, title="Simple task", description="")

        result = format_task(task)
        lines = result.split("\n")

        assert len(lines) == 1


class TestFormatTaskList:
    """Tests for format_task_list()."""

    def test_format_empty_task_list(self):
        """Test formatting an empty task list."""
        result = format_task_list([])

        assert "=== Your Tasks ===" in result
        assert "No tasks found" in result
        assert "Add your first task" in result

    def test_format_task_list_with_tasks(self):
        """Test formatting a list with tasks."""
        tasks = [
            Task(
                id=1, title="Buy groceries", description="Milk, eggs", completed=False
            ),
            Task(id=2, title="Call mom", completed=True),
            Task(id=3, title="Finish homework", completed=False),
        ]

        result = format_task_list(tasks)

        assert "=== Your Tasks ===" in result
        assert "#1" in result
        assert "#2" in result
        assert "#3" in result
        assert "Buy groceries" in result
        assert "Call mom" in result
        assert "Finish homework" in result

    def test_format_task_list_shows_summary(self):
        """Test that task list includes summary line."""
        tasks = [
            Task(id=1, title="Task 1", completed=False),
            Task(id=2, title="Task 2", completed=True),
            Task(id=3, title="Task 3", completed=False),
        ]

        result = format_task_list(tasks)

        assert "Total: 3 tasks" in result
        assert "1 completed" in result
        assert "2 pending" in result

    def test_format_task_list_shows_status_indicators(self):
        """Test that task list shows correct status indicators."""
        tasks = [
            Task(id=1, title="Pending task", completed=False),
            Task(id=2, title="Completed task", completed=True),
        ]

        result = format_task_list(tasks)

        assert "[ ]" in result
        assert "[x]" in result
