"""Integration tests for the Todo App CLI workflow."""

import pytest

from src.cli.formatters import format_task_list
from src.exceptions import TaskNotFoundError
from src.services.task_service import TaskService


class TestFullWorkflow:
    """Integration tests for complete user workflows."""

    def test_complete_workflow_add_complete_update_delete_view(self):
        """Test the complete workflow: add 3 tasks, complete 1, update 1, delete 1, view remaining.

        This test validates SC-007: Users can successfully complete a full workflow
        (add 3 tasks, complete 1, update 1, delete 1, view remaining) without errors.
        """
        service = TaskService()

        # Add 3 tasks
        task1 = service.add_task("Buy groceries", "Milk, eggs, bread")
        task2 = service.add_task("Call mom", "Wish her happy birthday")
        task3 = service.add_task("Finish homework", "Math assignment")

        assert len(service.list_tasks()) == 3

        # Complete task 1
        service.toggle_complete(task1.id)
        assert service.get_task(task1.id).completed is True

        # Update task 2
        service.update_task(
            task2.id, title="Call mom tonight", description="Birthday wishes"
        )
        updated_task = service.get_task(task2.id)
        assert updated_task.title == "Call mom tonight"
        assert updated_task.description == "Birthday wishes"

        # Delete task 3
        service.delete_task(task3.id)
        with pytest.raises(TaskNotFoundError):
            service.get_task(task3.id)

        # View remaining tasks
        remaining = service.list_tasks()
        assert len(remaining) == 2
        assert remaining[0].id == task1.id
        assert remaining[0].completed is True
        assert remaining[1].id == task2.id
        assert remaining[1].title == "Call mom tonight"

    def test_workflow_view_formatted_output(self):
        """Test that formatted output displays correctly after operations."""
        service = TaskService()

        # Add tasks
        service.add_task("Buy groceries", "Milk, eggs, bread")
        service.add_task("Call mom")
        service.add_task("Finish homework")

        # Complete one
        service.toggle_complete(2)

        # Get formatted output
        output = format_task_list(service.list_tasks())

        # Verify output contains expected elements
        assert "=== Your Tasks ===" in output
        assert "#1 [ ] Buy groceries" in output
        assert "#2 [x] Call mom" in output
        assert "#3 [ ] Finish homework" in output
        assert "Total: 3 tasks (1 completed, 2 pending)" in output

    def test_task_ids_remain_unique_after_deletion(self):
        """Test that task IDs remain unique even after deletions."""
        service = TaskService()

        # Add and delete tasks
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        service.delete_task(task1.id)

        # Add new task
        task3 = service.add_task("Task 3")

        # New task should have ID 3, not reuse ID 1
        assert task3.id == 3
        assert len(service.list_tasks()) == 2

    def test_toggle_complete_twice_returns_to_pending(self):
        """Test that toggling complete twice returns task to pending state."""
        service = TaskService()

        task = service.add_task("Test task")
        assert task.completed is False

        # Toggle to completed
        service.toggle_complete(task.id)
        assert service.get_task(task.id).completed is True

        # Toggle back to pending
        service.toggle_complete(task.id)
        assert service.get_task(task.id).completed is False

    def test_multiple_updates_accumulate(self):
        """Test that multiple updates work correctly."""
        service = TaskService()

        task = service.add_task("Original title", "Original description")

        # Update title only
        service.update_task(task.id, title="Updated title")
        assert service.get_task(task.id).title == "Updated title"
        assert service.get_task(task.id).description == "Original description"

        # Update description only
        service.update_task(task.id, description="Updated description")
        assert service.get_task(task.id).title == "Updated title"
        assert service.get_task(task.id).description == "Updated description"
