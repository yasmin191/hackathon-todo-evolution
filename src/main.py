"""Main entry point for the Todo App."""

import sys

from src.cli.formatters import format_error
from src.cli.menu import (
    display_menu,
    display_welcome,
    get_user_choice,
    handle_add_task,
    handle_delete_task,
    handle_exit,
    handle_toggle_complete,
    handle_update_task,
    handle_view_tasks,
)
from src.services.task_service import TaskService


def main() -> None:
    """Main application entry point."""
    service = TaskService()

    display_welcome()

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == "1":
            handle_add_task(service)
        elif choice == "2":
            handle_view_tasks(service)
        elif choice == "3":
            handle_toggle_complete(service)
        elif choice == "4":
            handle_update_task(service)
        elif choice == "5":
            handle_delete_task(service)
        elif choice == "6":
            handle_exit()
            sys.exit(0)
        else:
            print(format_error("Invalid choice. Please enter 1-6."))


if __name__ == "__main__":
    main()
