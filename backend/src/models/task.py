"""Task model and schemas."""

from datetime import UTC, datetime
from enum import Enum

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(UTC)


class Priority(str, Enum):
    """Task priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskBase(SQLModel):
    """Base task fields shared across schemas."""

    title: str = Field(min_length=1, max_length=500)
    description: str | None = Field(default=None)


class Task(TaskBase, table=True):
    """Task database model."""

    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    completed: bool = Field(default=False)
    priority: Priority = Field(default=Priority.MEDIUM)
    due_date: datetime | None = Field(default=None)
    reminder_at: datetime | None = Field(default=None)
    reminded: bool = Field(default=False)
    recurrence_rule: str | None = Field(default=None)
    parent_task_id: int | None = Field(default=None, foreign_key="tasks.id")
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class TaskCreate(SQLModel):
    """Schema for creating a new task."""

    title: str = Field(min_length=1, max_length=500)
    description: str | None = None
    priority: Priority = Priority.MEDIUM
    due_date: datetime | None = None
    reminder_at: datetime | None = None
    recurrence_rule: str | None = None


class TaskUpdate(SQLModel):
    """Schema for updating an existing task."""

    title: str | None = Field(default=None, min_length=1, max_length=500)
    description: str | None = None
    priority: Priority | None = None
    due_date: datetime | None = None
    reminder_at: datetime | None = None
    recurrence_rule: str | None = None


class TaskResponse(SQLModel):
    """Schema for task API responses."""

    id: int
    user_id: str
    title: str
    description: str | None
    completed: bool
    priority: Priority
    due_date: datetime | None
    reminder_at: datetime | None
    recurrence_rule: str | None
    created_at: datetime
    updated_at: datetime
    tags: list["TagResponse"] = []


class TagResponse(SQLModel):
    """Schema for tag in task response."""

    id: int
    name: str
    color: str
