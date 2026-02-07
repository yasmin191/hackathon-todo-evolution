"""Task management AI agent using OpenAI Agents SDK."""

from typing import Any

from sqlmodel import Session

from agents import Agent, Runner, function_tool
from src.agents.tools import TaskTools
from src.config import get_settings

settings = get_settings()

SYSTEM_PROMPT = """You are a helpful task management assistant. You help users manage their todo list through natural conversation.

You have access to the following tools:
- add_task: Create a new task with a title and optional description
- list_tasks: View tasks (can filter by status: all, pending, completed)
- get_task: Get details of a specific task by ID
- complete_task: Toggle a task's completion status (mark as complete/incomplete)
- delete_task: Remove a task permanently
- update_task: Change a task's title or description

Guidelines:
1. Be conversational and friendly
2. Confirm actions after they're completed
3. When listing tasks, show them in a clear format with IDs
4. If a user's request is ambiguous, ask for clarification
5. Keep responses concise but helpful
6. Use the appropriate tool for each action
7. If a task is not found, let the user know and suggest alternatives

Examples of user requests:
- "Add a task to buy milk" → Use add_task with title "Buy milk"
- "What do I need to do?" → Use list_tasks with status "pending"
- "Show all my tasks" → Use list_tasks with status "all"
- "I'm done with task 3" → Use complete_task with task_id 3
- "Delete the first task" → Use delete_task with task_id 1
- "Rename task 2 to 'Call mom'" → Use update_task with task_id 2, title "Call mom"
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
        def add_task(title: str, description: str | None = None) -> dict[str, Any]:
            """Create a new task.

            Args:
                title: The task title (required)
                description: Optional task description
            """
            return self.tools.add_task(title, description)

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
        ) -> dict[str, Any]:
            """Update a task's title or description.

            Args:
                task_id: The ID of the task to update
                title: New title (optional)
                description: New description (optional)
            """
            return self.tools.update_task(task_id, title, description)

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
