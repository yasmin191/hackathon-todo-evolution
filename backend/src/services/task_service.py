"""Task business logic service."""

from datetime import UTC, datetime

from sqlmodel import Session, or_, select

from src.models.tag import Tag, TaskTag
from src.models.task import Priority, Task, TaskCreate, TaskUpdate


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
            priority=data.priority,
            due_date=data.due_date,
            reminder_at=data.reminder_at,
            recurrence_rule=data.recurrence_rule,
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_tasks(
        self,
        user_id: str,
        status: str | None = None,
        priority: Priority | None = None,
        tag: str | None = None,
        search: str | None = None,
        due_before: datetime | None = None,
        overdue: bool = False,
        sort: str = "created_at",
        order: str = "desc",
    ) -> list[Task]:
        """Get tasks for a user with optional filters."""
        statement = select(Task).where(Task.user_id == user_id)

        # Status filter
        if status == "completed":
            statement = statement.where(Task.completed == True)  # noqa: E712
        elif status == "incomplete":
            statement = statement.where(Task.completed == False)  # noqa: E712

        # Priority filter
        if priority:
            statement = statement.where(Task.priority == priority)

        # Tag filter
        if tag:
            statement = (
                statement.join(TaskTag, Task.id == TaskTag.task_id)
                .join(Tag, TaskTag.tag_id == Tag.id)
                .where(Tag.name == tag)
            )

        # Search filter (title or description contains search term)
        if search:
            search_pattern = f"%{search}%"
            statement = statement.where(
                or_(
                    Task.title.ilike(search_pattern),
                    Task.description.ilike(search_pattern),
                )
            )

        # Due date filter
        if due_before:
            statement = statement.where(Task.due_date <= due_before)

        # Overdue filter
        if overdue:
            now = datetime.now(UTC)
            statement = statement.where(
                Task.due_date < now,
                Task.completed == False,  # noqa: E712
            )

        # Sorting
        sort_column = getattr(Task, sort, Task.created_at)
        if order == "asc":
            statement = statement.order_by(sort_column.asc())
        else:
            statement = statement.order_by(sort_column.desc())

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

        # Delete tag associations first
        stmt = select(TaskTag).where(TaskTag.task_id == task_id)
        associations = self.session.exec(stmt).all()
        for assoc in associations:
            self.session.delete(assoc)

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

    def get_tasks_needing_reminder(self) -> list[Task]:
        """Get tasks that need reminder notifications."""
        now = datetime.now(UTC)
        statement = select(Task).where(
            Task.reminder_at <= now,
            Task.reminded == False,  # noqa: E712
            Task.completed == False,  # noqa: E712
        )
        return list(self.session.exec(statement).all())

    def mark_reminded(self, task_id: int) -> None:
        """Mark a task as reminded."""
        task = self.session.get(Task, task_id)
        if task:
            task.reminded = True
            self.session.add(task)
            self.session.commit()
