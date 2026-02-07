"""Unit tests for the Task model."""

from datetime import datetime

import pytest

from src.exceptions import ValidationError
from src.models.task import Task


class TestTaskCreation:
    """Tests for Task creation and validation."""

    def test_create_task_with_title_only(self):
        """Test creating a task with just a title."""
        task = Task(id=1, title="Buy groceries")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == ""
        assert task.completed is False
        assert isinstance(task.created_at, datetime)

    def test_create_task_with_title_and_description(self):
        """Test creating a task with title and description."""
        task = Task(id=1, title="Buy groceries", description="Milk, eggs, bread")

        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"

    def test_create_task_with_empty_title_raises_error(self):
        """Test that empty title raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Task(id=1, title="")

        assert "Title is required" in str(exc_info.value)

    def test_create_task_with_whitespace_only_title_raises_error(self):
        """Test that whitespace-only title raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Task(id=1, title="   ")

        assert "Title is required" in str(exc_info.value)

    def test_create_task_with_title_exceeding_500_chars_raises_error(self):
        """Test that title over 500 characters raises ValidationError."""
        long_title = "x" * 501

        with pytest.raises(ValidationError) as exc_info:
            Task(id=1, title=long_title)

        assert "500 characters or less" in str(exc_info.value)

    def test_create_task_with_title_exactly_500_chars_succeeds(self):
        """Test that title with exactly 500 characters is accepted."""
        title = "x" * 500
        task = Task(id=1, title=title)

        assert len(task.title) == 500


class TestTaskToggleComplete:
    """Tests for Task completion toggle."""

    def test_toggle_complete_from_pending_to_completed(self):
        """Test toggling a pending task to completed."""
        task = Task(id=1, title="Test task")
        assert task.completed is False

        task.toggle_complete()

        assert task.completed is True

    def test_toggle_complete_from_completed_to_pending(self):
        """Test toggling a completed task to pending."""
        task = Task(id=1, title="Test task", completed=True)
        assert task.completed is True

        task.toggle_complete()

        assert task.completed is False

    def test_toggle_complete_twice_returns_to_original(self):
        """Test that toggling twice returns to original state."""
        task = Task(id=1, title="Test task")
        original_status = task.completed

        task.toggle_complete()
        task.toggle_complete()

        assert task.completed == original_status
