"""Task model and schemas."""

from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(UTC)


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
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class TaskCreate(SQLModel):
    """Schema for creating a new task."""

    title: str = Field(min_length=1, max_length=500)
    description: str | None = None


class TaskUpdate(SQLModel):
    """Schema for updating an existing task."""

    title: str | None = Field(default=None, min_length=1, max_length=500)
    description: str | None = None


class TaskResponse(SQLModel):
    """Schema for task API responses."""

    id: int
    user_id: str
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime
