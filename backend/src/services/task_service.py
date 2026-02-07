"""Task business logic service."""

from datetime import UTC, datetime

from sqlmodel import Session, select

from src.models.task import Task, TaskCreate, TaskUpdate


class TaskService:
    """Service for task CRUD operations."""

    def __init__(self, session: Session):
        self.session = session

    def create_task(self, user_id: str, data: TaskCreate) -> Task:
        """Create a new task for the user."""
        task = Task(
            user_id=user_id,
            title=data.title,
            description=data.description,
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_tasks(self, user_id: str) -> list[Task]:
        """Get all tasks for a user."""
        statement = select(Task).where(Task.user_id == user_id)
        return list(self.session.exec(statement).all())

    def get_task(self, user_id: str, task_id: int) -> Task | None:
        """Get a specific task by ID for a user."""
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.id == task_id,
        )
        return self.session.exec(statement).first()

    def update_task(self, user_id: str, task_id: int, data: TaskUpdate) -> Task | None:
        """Update a task's title and/or description."""
        task = self.get_task(user_id, task_id)
        if not task:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)

        task.updated_at = datetime.now(UTC)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, user_id: str, task_id: int) -> bool:
        """Delete a task by ID."""
        task = self.get_task(user_id, task_id)
        if not task:
            return False

        self.session.delete(task)
        self.session.commit()
        return True

    def toggle_complete(self, user_id: str, task_id: int) -> Task | None:
        """Toggle a task's completed status."""
        task = self.get_task(user_id, task_id)
        if not task:
            return None

        task.completed = not task.completed
        task.updated_at = datetime.now(UTC)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task
