"""Unit tests for the TaskService."""

import pytest

from src.exceptions import TaskNotFoundError, ValidationError
from src.models.task import Task
from src.services.task_service import TaskService


class TestAddTask:
    """Tests for TaskService.add_task()."""

    def test_add_task_returns_task_with_id(self, task_service):
        """Test that add_task returns a task with assigned ID."""
        task = task_service.add_task("Buy groceries")

        assert task.id == 1
        assert task.title == "Buy groceries"

    def test_add_task_with_description(self, task_service):
        """Test adding a task with description."""
        task = task_service.add_task("Buy groceries", "Milk, eggs, bread")

        assert task.description == "Milk, eggs, bread"

    def test_add_multiple_tasks_increments_id(self, task_service):
        """Test that each new task gets incremented ID."""
        task1 = task_service.add_task("Task 1")
        task2 = task_service.add_task("Task 2")
        task3 = task_service.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_strips_whitespace_from_title(self, task_service):
        """Test that whitespace is stripped from title."""
        task = task_service.add_task("  Buy groceries  ")

        assert task.title == "Buy groceries"

    def test_add_task_with_empty_title_raises_error(self, task_service):
        """Test that empty title raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            task_service.add_task("")

        assert "Title is required" in str(exc_info.value)

    def test_add_task_with_title_over_500_chars_raises_error(self, task_service):
        """Test that title over 500 characters raises ValidationError."""
        long_title = "x" * 501

        with pytest.raises(ValidationError) as exc_info:
            task_service.add_task(long_title)

        assert "500 characters or less" in str(exc_info.value)


class TestListTasks:
    """Tests for TaskService.list_tasks()."""

    def test_list_tasks_empty_returns_empty_list(self, task_service):
        """Test that list_tasks returns empty list when no tasks."""
        tasks = task_service.list_tasks()

        assert tasks == []

    def test_list_tasks_returns_all_tasks(self, task_service):
        """Test that list_tasks returns all added tasks."""
        task_service.add_task("Task 1")
        task_service.add_task("Task 2")
        task_service.add_task("Task 3")

        tasks = task_service.list_tasks()

        assert len(tasks) == 3
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"
        assert tasks[2].title == "Task 3"

    def test_list_tasks_returns_tasks_in_creation_order(self, task_service_with_tasks):
        """Test that tasks are returned in creation order."""
        tasks = task_service_with_tasks.list_tasks()

        assert tasks[0].title == "Buy groceries"
        assert tasks[1].title == "Call mom"
        assert tasks[2].title == "Finish homework"


class TestGetTask:
    """Tests for TaskService.get_task()."""

    def test_get_task_returns_correct_task(self, task_service):
        """Test that get_task returns the correct task by ID."""
        task_service.add_task("Task 1")
        task_service.add_task("Task 2")

        task = task_service.get_task(2)

        assert task.id == 2
        assert task.title == "Task 2"

    def test_get_task_not_found_raises_error(self, task_service):
        """Test that get_task raises error for non-existent ID."""
        with pytest.raises(TaskNotFoundError) as exc_info:
            task_service.get_task(999)

        assert "Task not found: #999" in str(exc_info.value)


class TestToggleComplete:
    """Tests for TaskService.toggle_complete()."""

    def test_toggle_complete_marks_pending_as_completed(self, task_service):
        """Test toggling a pending task to completed."""
        task = task_service.add_task("Test task")
        assert task.completed is False

        updated_task = task_service.toggle_complete(1)

        assert updated_task.completed is True

    def test_toggle_complete_marks_completed_as_pending(self, task_service):
        """Test toggling a completed task to pending."""
        task = task_service.add_task("Test task")
        task_service.toggle_complete(1)  # Mark as completed

        updated_task = task_service.toggle_complete(1)  # Toggle back

        assert updated_task.completed is False

    def test_toggle_complete_not_found_raises_error(self, task_service):
        """Test that toggle_complete raises error for non-existent ID."""
        with pytest.raises(TaskNotFoundError) as exc_info:
            task_service.toggle_complete(999)

        assert "Task not found: #999" in str(exc_info.value)


class TestUpdateTask:
    """Tests for TaskService.update_task()."""

    def test_update_task_title(self, task_service):
        """Test updating only the task title."""
        task_service.add_task("Old title", "Description")

        updated = task_service.update_task(1, title="New title")

        assert updated.title == "New title"
        assert updated.description == "Description"

    def test_update_task_description(self, task_service):
        """Test updating only the task description."""
        task_service.add_task("Title", "Old description")

        updated = task_service.update_task(1, description="New description")

        assert updated.title == "Title"
        assert updated.description == "New description"

    def test_update_task_both_fields(self, task_service):
        """Test updating both title and description."""
        task_service.add_task("Old title", "Old description")

        updated = task_service.update_task(
            1, title="New title", description="New description"
        )

        assert updated.title == "New title"
        assert updated.description == "New description"

    def test_update_task_with_none_keeps_current(self, task_service):
        """Test that None values keep current field values."""
        task_service.add_task("Title", "Description")

        updated = task_service.update_task(1, title=None, description=None)

        assert updated.title == "Title"
        assert updated.description == "Description"

    def test_update_task_not_found_raises_error(self, task_service):
        """Test that update_task raises error for non-existent ID."""
        with pytest.raises(TaskNotFoundError) as exc_info:
            task_service.update_task(999, title="New title")

        assert "Task not found: #999" in str(exc_info.value)

    def test_update_task_with_invalid_title_raises_error(self, task_service):
        """Test that update_task validates the new title."""
        task_service.add_task("Original title")
        long_title = "x" * 501

        with pytest.raises(ValidationError) as exc_info:
            task_service.update_task(1, title=long_title)

        assert "500 characters or less" in str(exc_info.value)


class TestDeleteTask:
    """Tests for TaskService.delete_task()."""

    def test_delete_task_removes_from_storage(self, task_service):
        """Test that delete_task removes the task."""
        task_service.add_task("Task 1")
        task_service.add_task("Task 2")

        task_service.delete_task(1)

        tasks = task_service.list_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == 2

    def test_delete_task_not_found_raises_error(self, task_service):
        """Test that delete_task raises error for non-existent ID."""
        with pytest.raises(TaskNotFoundError) as exc_info:
            task_service.delete_task(999)

        assert "Task not found: #999" in str(exc_info.value)

    def test_deleted_task_cannot_be_retrieved(self, task_service):
        """Test that deleted task cannot be retrieved."""
        task_service.add_task("Task to delete")
        task_service.delete_task(1)

        with pytest.raises(TaskNotFoundError):
            task_service.get_task(1)
