"""Shared pytest fixtures for Todo App tests."""

import pytest
from src.services.task_service import TaskService


@pytest.fixture
def task_service():
    """Create a fresh TaskService instance for each test."""
    return TaskService()


@pytest.fixture
def task_service_with_tasks(task_service):
    """Create a TaskService with sample tasks."""
    task_service.add_task("Buy groceries", "Milk, eggs, bread")
    task_service.add_task("Call mom", "Wish her happy birthday")
    task_service.add_task("Finish homework", "")
    return task_service
