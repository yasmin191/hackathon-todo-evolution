"""Task management tools for the AI agent."""

from typing import Any

from sqlmodel import Session

from src.models.task import Task, TaskCreate, TaskUpdate
from src.services.task_service import TaskService


def format_task(task: Task) -> str:
    """Format a task for display in chat."""
    status = "✓" if task.completed else "○"
    desc = f" - {task.description}" if task.description else ""
    return f"{status} [{task.id}] {task.title}{desc}"


def format_task_list(tasks: list[Task]) -> str:
    """Format a list of tasks for display in chat."""
    if not tasks:
        return "You have no tasks."
    return "\n".join(format_task(task) for task in tasks)


class TaskTools:
    """Task management tools that can be called by the AI agent."""

    def __init__(self, session: Session, user_id: str):
        self.service = TaskService(session)
        self.user_id = user_id

    def add_task(self, title: str, description: str | None = None) -> dict[str, Any]:
        """Create a new task.

        Args:
            title: The task title (required)
            description: Optional task description

        Returns:
            Success message with task details
        """
        data = TaskCreate(title=title, description=description)
        task = self.service.create_task(self.user_id, data)
        return {
            "success": True,
            "message": f"Created task: {task.title}",
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
            },
        }

    def list_tasks(self, status: str = "all") -> dict[str, Any]:
        """Get all tasks for the user.

        Args:
            status: Filter by status - "all", "pending", or "completed"

        Returns:
            List of tasks with their details
        """
        tasks = self.service.get_tasks(self.user_id)

        if status == "pending":
            tasks = [t for t in tasks if not t.completed]
        elif status == "completed":
            tasks = [t for t in tasks if t.completed]

        return {
            "success": True,
            "count": len(tasks),
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "completed": t.completed,
                }
                for t in tasks
            ],
            "formatted": format_task_list(tasks),
        }

    def get_task(self, task_id: int) -> dict[str, Any]:
        """Get a specific task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Task details or error if not found
        """
        task = self.service.get_task(self.user_id, task_id)
        if not task:
            return {"success": False, "error": f"Task {task_id} not found"}

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
            },
        }

    def complete_task(self, task_id: int) -> dict[str, Any]:
        """Toggle a task's completion status.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            Updated task status or error if not found
        """
        task = self.service.toggle_complete(self.user_id, task_id)
        if not task:
            return {"success": False, "error": f"Task {task_id} not found"}

        status = "completed" if task.completed else "incomplete"
        return {
            "success": True,
            "message": f"Marked task '{task.title}' as {status}",
            "task": {
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
            },
        }

    def delete_task(self, task_id: int) -> dict[str, Any]:
        """Delete a task.

        Args:
            task_id: The ID of the task to delete

        Returns:
            Success message or error if not found
        """
        task = self.service.get_task(self.user_id, task_id)
        if not task:
            return {"success": False, "error": f"Task {task_id} not found"}

        title = task.title
        self.service.delete_task(self.user_id, task_id)
        return {
            "success": True,
            "message": f"Deleted task: {title}",
        }

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        """Update a task's title or description.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            Updated task details or error if not found
        """
        data = TaskUpdate(title=title, description=description)
        task = self.service.update_task(self.user_id, task_id, data)
        if not task:
            return {"success": False, "error": f"Task {task_id} not found"}

        return {
            "success": True,
            "message": f"Updated task: {task.title}",
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
            },
        }
