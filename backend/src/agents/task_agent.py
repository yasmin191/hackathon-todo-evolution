"""Task management AI agent using OpenAI Agents SDK."""

from typing import Any

from sqlmodel import Session

from agents import Agent, Runner, function_tool
from src.agents.tools import TaskTools
from src.config import get_settings

settings = get_settings()

SYSTEM_PROMPT = """You are a helpful task management assistant. You help users manage their todo list through natural conversation.

You have access to the following tools:
- add_task: Create a new task with title, description, priority, due date, tags, and recurrence
- list_tasks: View tasks (can filter by status: all, pending, completed)
- get_task: Get details of a specific task by ID
- complete_task: Toggle a task's completion status (mark as complete/incomplete)
- delete_task: Remove a task permanently
- update_task: Change a task's title, description, priority, or due date
- search_tasks: Search tasks by title or description keywords
- filter_tasks: Filter tasks by priority, tag, or show only overdue tasks
- add_tag_to_task: Add a tag to an existing task
- list_tags: Show all available tags

Priority Levels: low, medium (default), high, urgent

Due Dates: You can understand natural language dates like "tomorrow", "next monday", "in 3 days", "january 15th"

Recurrence Patterns:
- DAILY: Task repeats every day
- WEEKLY:MON,WED,FRI: Task repeats on specific weekdays
- MONTHLY:15: Task repeats on the 15th of each month
- CUSTOM:7: Task repeats every 7 days

Guidelines:
1. Be conversational and friendly
2. Confirm actions after they're completed
3. When listing tasks, show them in a clear format with IDs, priority, and due dates
4. If a user's request is ambiguous, ask for clarification
5. Keep responses concise but helpful
6. Use the appropriate tool for each action
7. If a task is not found, let the user know and suggest alternatives
8. When users mention urgency or importance, set appropriate priority
9. When users mention deadlines, set the due date

Examples of user requests:
- "Add a task to buy milk" → Use add_task with title "Buy milk"
- "Add a high priority task to review the report" → Use add_task with priority "high"
- "Add task to call mom tomorrow" → Use add_task with due_date "tomorrow"
- "Add a daily task to take vitamins" → Use add_task with recurrence "DAILY"
- "Add task buy groceries with tag shopping" → Use add_task with tags ["shopping"]
- "What do I need to do?" → Use list_tasks with status "pending"
- "Show all my tasks" → Use list_tasks with status "all"
- "I'm done with task 3" → Use complete_task with task_id 3
- "Delete the first task" → Use delete_task with task_id 1
- "Rename task 2 to 'Call mom'" → Use update_task with task_id 2, title "Call mom"
- "Find tasks about meeting" → Use search_tasks with query "meeting"
- "Show my urgent tasks" → Use filter_tasks with priority "urgent"
- "What's overdue?" → Use filter_tasks with overdue True
- "Show tasks tagged with work" → Use filter_tasks with tag "work"
- "Tag task 5 as personal" → Use add_tag_to_task with task_id 5, tag_name "personal"
"""


class TaskAgent:
    """AI agent for task management via natural language."""

    def __init__(self, session: Session, user_id: str):
        self.session = session
        self.user_id = user_id
        self.tools = TaskTools(session, user_id)
        self._agent = self._create_agent()

    def _create_agent(self) -> Agent:
        """Create the OpenAI agent with task tools."""

        # Create function tools from TaskTools methods
        @function_tool
        def add_task(
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
                recurrence: Recurrence pattern (e.g., "DAILY", "WEEKLY:MON,WED")
            """
            return self.tools.add_task(
                title, description, priority, due_date, tags, recurrence
            )

        @function_tool
        def list_tasks(status: str = "all") -> dict[str, Any]:
            """Get all tasks for the user.

            Args:
                status: Filter by status - "all", "pending", or "completed"
            """
            return self.tools.list_tasks(status)

        @function_tool
        def get_task(task_id: int) -> dict[str, Any]:
            """Get a specific task by ID.

            Args:
                task_id: The ID of the task to retrieve
            """
            return self.tools.get_task(task_id)

        @function_tool
        def complete_task(task_id: int) -> dict[str, Any]:
            """Toggle a task's completion status.

            Args:
                task_id: The ID of the task to toggle
            """
            return self.tools.complete_task(task_id)

        @function_tool
        def delete_task(task_id: int) -> dict[str, Any]:
            """Delete a task.

            Args:
                task_id: The ID of the task to delete
            """
            return self.tools.delete_task(task_id)

        @function_tool
        def update_task(
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
                priority: New priority level (optional)
                due_date: New due date (optional)
            """
            return self.tools.update_task(
                task_id, title, description, priority, due_date
            )

        @function_tool
        def search_tasks(query: str) -> dict[str, Any]:
            """Search tasks by title or description.

            Args:
                query: Search term to find in task titles or descriptions
            """
            return self.tools.search_tasks(query)

        @function_tool
        def filter_tasks(
            priority: str | None = None,
            tag: str | None = None,
            overdue: bool = False,
        ) -> dict[str, Any]:
            """Filter tasks by various criteria.

            Args:
                priority: Filter by priority - "low", "medium", "high", "urgent"
                tag: Filter by tag name
                overdue: If True, show only overdue tasks
            """
            return self.tools.filter_tasks(priority, tag, overdue)

        @function_tool
        def add_tag_to_task(task_id: int, tag_name: str) -> dict[str, Any]:
            """Add a tag to a task.

            Args:
                task_id: The ID of the task
                tag_name: Name of the tag to add
            """
            return self.tools.add_tag_to_task(task_id, tag_name)

        @function_tool
        def list_tags() -> dict[str, Any]:
            """List all tags for the user."""
            return self.tools.list_tags()

        return Agent(
            name="TaskAssistant",
            instructions=SYSTEM_PROMPT,
            tools=[
                add_task,
                list_tasks,
                get_task,
                complete_task,
                delete_task,
                update_task,
                search_tasks,
                filter_tasks,
                add_tag_to_task,
                list_tags,
            ],
            model=settings.openai_model,
        )

    async def run(
        self, message: str, history: list[dict[str, str]] | None = None
    ) -> str:
        """Run the agent with a user message.

        Args:
            message: The user's message
            history: Optional conversation history

        Returns:
            The agent's response
        """
        # Build messages list with history
        messages = []
        if history:
            for msg in history:
                messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": message})

        # Run the agent
        result = await Runner.run(self._agent, messages)

        # Extract the final response
        return result.final_output


async def run_agent(
    session: Session,
    user_id: str,
    message: str,
    history: list[dict[str, str]] | None = None,
) -> str:
    """Convenience function to run the task agent.

    Args:
        session: Database session
        user_id: The user's ID
        message: The user's message
        history: Optional conversation history

    Returns:
        The agent's response
    """
    agent = TaskAgent(session, user_id)
    return await agent.run(message, history)
