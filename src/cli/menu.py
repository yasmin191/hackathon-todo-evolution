"""Menu display and input handling for the Todo App CLI."""

from src.cli.formatters import format_error, format_success, format_task_list
from src.exceptions import TaskNotFoundError, ValidationError
from src.services.task_service import TaskService

MENU = """
╔══════════════════════════════════╗
║         TODO APP - Phase I       ║
╠══════════════════════════════════╣
║  1. Add Task                     ║
║  2. View All Tasks               ║
║  3. Mark Task Complete/Incomplete║
║  4. Update Task                  ║
║  5. Delete Task                  ║
║  6. Exit                         ║
╚══════════════════════════════════╝
"""

WELCOME_BANNER = """
╔══════════════════════════════════╗
║         TODO APP - Phase I       ║
║    Welcome! Your tasks await.    ║
╚══════════════════════════════════╝
"""


def display_menu() -> None:
    """Display the main menu options."""
    print(MENU)


def display_welcome() -> None:
    """Display the welcome banner."""
    print(WELCOME_BANNER)


def get_user_choice() -> str:
    """Get the user's menu choice.

    Returns:
        The user's input string
    """
    return input("Enter your choice (1-6): ").strip()


def get_task_id_input(prompt: str = "Enter task ID: ") -> int:
    """Get a valid task ID from user input.

    Args:
        prompt: The prompt to display

    Returns:
        The validated task ID

    Raises:
        ValidationError: If input is not a valid positive integer
    """
    user_input = input(prompt).strip()

    try:
        task_id = int(user_input)
        if task_id <= 0:
            raise ValidationError("Invalid ID: please enter a number")
        return task_id
    except ValueError:
        raise ValidationError("Invalid ID: please enter a number")


def handle_add_task(service: TaskService) -> None:
    """Handle the add task menu option.

    Args:
        service: The TaskService instance
    """
    print("\n=== Add New Task ===")

    title = input("Enter task title: ").strip()
    if not title:
        print(format_error("Title is required"))
        return

    description = input("Enter description (optional, press Enter to skip): ").strip()

    try:
        task = service.add_task(title, description)
        print(format_success(f"Task created: #{task.id} - {task.title}"))
    except ValidationError as e:
        print(format_error(str(e)))


def handle_view_tasks(service: TaskService) -> None:
    """Handle the view all tasks menu option.

    Args:
        service: The TaskService instance
    """
    print()
    tasks = service.list_tasks()
    print(format_task_list(tasks))


def handle_toggle_complete(service: TaskService) -> None:
    """Handle the mark complete/incomplete menu option.

    Args:
        service: The TaskService instance
    """
    print("\n=== Toggle Task Completion ===")

    try:
        task_id = get_task_id_input()
        task = service.toggle_complete(task_id)
        status = "completed" if task.completed else "pending"
        print(format_success(f"Task #{task.id} marked as {status}"))
    except (ValidationError, TaskNotFoundError) as e:
        print(format_error(str(e)))


def handle_update_task(service: TaskService) -> None:
    """Handle the update task menu option.

    Args:
        service: The TaskService instance
    """
    print("\n=== Update Task ===")

    try:
        task_id = get_task_id_input()
        task = service.get_task(task_id)

        print(f"\nCurrent task: #{task.id} - {task.title}")
        if task.description:
            print(f"Current description: {task.description}")

        new_title = input("\nEnter new title (press Enter to keep current): ").strip()
        new_description = input("Enter new description (press Enter to keep current): ").strip()
        new_description = input(
            "Enter new description (press Enter to keep current): "
        ).strip()

        # Only update if user provided new values
        title_to_update = new_title if new_title else None
        desc_to_update = new_description if new_description else None

        if title_to_update or desc_to_update is not None:
            service.update_task(
                task_id, title_to_update, desc_to_update if new_description else None
            )
            print(format_success(f"Task #{task.id} updated successfully"))
        else:
            print("No changes made.")

    except (ValidationError, TaskNotFoundError) as e:
        print(format_error(str(e)))


def handle_delete_task(service: TaskService) -> None:
    """Handle the delete task menu option.

    Args:
        service: The TaskService instance
    """
    print("\n=== Delete Task ===")

    try:
        task_id = get_task_id_input()
        task = service.get_task(task_id)

        confirm = (
            input(
                f'\nAre you sure you want to delete "#{task.id} - {task.title}"? (y/n): '
            )
            .strip()
            .lower()
        )

        if confirm == "y":
            print(format_success(f"Task deleted: #{task_id}"))
        else:
            print("\nDeletion cancelled.")

    except (ValidationError, TaskNotFoundError) as e:
        print(format_error(str(e)))


def handle_exit() -> None:
    """Handle the exit menu option."""
    print("\nThank you for using Todo App. Goodbye!")
