"""Task management tools for the AI agent."""

from typing import Any

from dateparser import parse as parse_date
from sqlmodel import Session

from src.models.task import Priority, Task, TaskCreate, TaskUpdate
from src.services import tag_service
from src.services.task_service import TaskService

PRIORITY_MAP = {
    "low": Priority.LOW,
    "medium": Priority.MEDIUM,
    "high": Priority.HIGH,
    "urgent": Priority.URGENT,
}


def format_task(task: Task, tags: list | None = None) -> str:
    """Format a task for display in chat."""
    status = "✓" if task.completed else "○"
    priority_icon = {"urgent": "🔴", "high": "🟠", "medium": "🔵", "low": "⚪"}.get(
        task.priority.value, ""
    )
    desc = f" - {task.description}" if task.description else ""
    due = f" (due: {task.due_date.strftime('%Y-%m-%d')})" if task.due_date else ""
    tag_str = f" [{', '.join(t.name for t in tags)}]" if tags else ""
    return f"{status} {priority_icon} [{task.id}] {task.title}{desc}{due}{tag_str}"


def format_task_list(tasks: list[Task], session=None) -> str:
    """Format a list of tasks for display in chat."""
    if not tasks:
        return "You have no tasks."
    result = []
    for task in tasks:
        tags = tag_service.get_task_tags(session, task.id) if session else None
        result.append(format_task(task, tags))
    return "\n".join(result)


class TaskTools:
    """Task management tools that can be called by the AI agent."""

    def __init__(self, session: Session, user_id: str):
        self.session = session
        self.service = TaskService(session)
        self.user_id = user_id

    def add_task(
        self,
        title: str,
        description: str | None = None,
        priority: str = "medium",
        due_date: str | None = None,
        tags: list[str] | None = None,
        recurrence: str | None = None,
    ) -> dict[str, Any]:
        """Create a new task.

        Args:
            title: The task title (required)
            description: Optional task description
            priority: Priority level - "low", "medium", "high", "urgent"
            due_date: Due date (e.g., "tomorrow", "next monday", "2026-01-20")
            tags: List of tag names to add to the task
            recurrence: Recurrence pattern (e.g., "DAILY", "WEEKLY:MON,WED", "MONTHLY:15")

        Returns:
            Success message with task details
        """
        # Parse priority
        priority_enum = PRIORITY_MAP.get(priority.lower(), Priority.MEDIUM)

        # Parse due date
        parsed_due = None
        if due_date:
            parsed_due = parse_date(due_date)

        data = TaskCreate(
            title=title,
            description=description,
            priority=priority_enum,
            due_date=parsed_due,
            recurrence_rule=recurrence,
        )
        task = self.service.create_task(self.user_id, data)

        # Add tags if provided
        if tags:
            tag_ids = []
            for tag_name in tags:
                tag = tag_service.get_or_create_tag(
                    self.session, self.user_id, tag_name
                )
                tag_ids.append(tag.id)
            tag_service.add_tags_to_task(self.session, task.id, tag_ids)

        return {
            "success": True,
            "message": f"Created task: {task.title}",
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority.value,
                "due_date": task.due_date.isoformat() if task.due_date else None,
            },
        }

    def list_tasks(self, status: str = "all") -> dict[str, Any]:
        """Get all tasks for the user.

        Args:
            status: Filter by status - "all", "pending", or "completed"

        Returns:
            List of tasks with their details
        """
        status_filter = None
        if status == "pending":
            status_filter = "incomplete"
        elif status == "completed":
            status_filter = "completed"

        tasks = self.service.get_tasks(self.user_id, status=status_filter)

        return {
            "success": True,
            "count": len(tasks),
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "completed": t.completed,
                    "priority": t.priority.value,
                    "due_date": t.due_date.isoformat() if t.due_date else None,
                }
                for t in tasks
            ],
            "formatted": format_task_list(tasks, self.session),
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
        priority: str | None = None,
        due_date: str | None = None,
    ) -> dict[str, Any]:
        """Update a task's properties.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)
            priority: New priority - "low", "medium", "high", "urgent" (optional)
            due_date: New due date (optional)

        Returns:
            Updated task details or error if not found
        """
        # Parse priority if provided
        priority_enum = None
        if priority:
            priority_enum = PRIORITY_MAP.get(priority.lower())

        # Parse due date if provided
        parsed_due = None
        if due_date:
            parsed_due = parse_date(due_date)

        data = TaskUpdate(
            title=title,
            description=description,
            priority=priority_enum,
            due_date=parsed_due,
        )
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
                "priority": task.priority.value,
                "due_date": task.due_date.isoformat() if task.due_date else None,
            },
        }

    def search_tasks(self, query: str) -> dict[str, Any]:
        """Search tasks by title or description.

        Args:
            query: Search term to find in task titles or descriptions

        Returns:
            List of matching tasks
        """
        tasks = self.service.get_tasks(self.user_id, search=query)

        return {
            "success": True,
            "count": len(tasks),
            "query": query,
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "completed": t.completed,
                    "priority": t.priority.value,
                }
                for t in tasks
            ],
            "formatted": format_task_list(tasks, self.session),
        }

    def filter_tasks(
        self,
        priority: str | None = None,
        tag: str | None = None,
        overdue: bool = False,
    ) -> dict[str, Any]:
        """Filter tasks by various criteria.

        Args:
            priority: Filter by priority - "low", "medium", "high", "urgent"
            tag: Filter by tag name
            overdue: If True, show only overdue tasks

        Returns:
            List of filtered tasks
        """
        priority_enum = None
        if priority:
            priority_enum = PRIORITY_MAP.get(priority.lower())

        tasks = self.service.get_tasks(
            self.user_id,
            priority=priority_enum,
            tag=tag,
            overdue=overdue,
        )

        filter_desc = []
        if priority:
            filter_desc.append(f"priority={priority}")
        if tag:
            filter_desc.append(f"tag={tag}")
        if overdue:
            filter_desc.append("overdue")

        return {
            "success": True,
            "count": len(tasks),
            "filters": filter_desc,
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "completed": t.completed,
                    "priority": t.priority.value,
                    "due_date": t.due_date.isoformat() if t.due_date else None,
                }
                for t in tasks
            ],
            "formatted": format_task_list(tasks, self.session),
        }

    def add_tag_to_task(self, task_id: int, tag_name: str) -> dict[str, Any]:
        """Add a tag to a task.

        Args:
            task_id: The ID of the task
            tag_name: Name of the tag to add

        Returns:
            Success message or error
        """
        task = self.service.get_task(self.user_id, task_id)
        if not task:
            return {"success": False, "error": f"Task {task_id} not found"}

        tag = tag_service.get_or_create_tag(self.session, self.user_id, tag_name)
        tag_service.add_tags_to_task(self.session, task_id, [tag.id])

        return {
            "success": True,
            "message": f"Added tag '{tag_name}' to task '{task.title}'",
        }

    def list_tags(self) -> dict[str, Any]:
        """List all tags for the user.

        Returns:
            List of all user's tags
        """
        tags = tag_service.get_tags(self.session, self.user_id)

        return {
            "success": True,
            "count": len(tags),
            "tags": [{"id": t.id, "name": t.name, "color": t.color} for t in tags],
        }
