"""Tag model and schemas."""

from datetime import UTC, datetime

from sqlmodel import Field, SQLModel, UniqueConstraint


def utc_now() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(UTC)


class Tag(SQLModel, table=True):
    """Tag database model."""

    __tablename__ = "tags"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_user_tag_name"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    name: str = Field(max_length=50)
    color: str = Field(default="#6366f1", max_length=7)
    created_at: datetime = Field(default_factory=utc_now)


class TaskTag(SQLModel, table=True):
    """Junction table for task-tag many-to-many relationship."""

    __tablename__ = "task_tags"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True, ondelete="CASCADE")
    tag_id: int = Field(foreign_key="tags.id", primary_key=True, ondelete="CASCADE")


class TagCreate(SQLModel):
    """Schema for creating a new tag."""

    name: str = Field(min_length=1, max_length=50)
    color: str = Field(default="#6366f1", max_length=7)


class TagUpdate(SQLModel):
    """Schema for updating an existing tag."""

    name: str | None = Field(default=None, min_length=1, max_length=50)
    color: str | None = Field(default=None, max_length=7)


class TagResponse(SQLModel):
    """Schema for tag API responses."""

    id: int
    user_id: str
    name: str
    color: str
    created_at: datetime


class TaskTagsUpdate(SQLModel):
    """Schema for adding tags to a task."""

    tag_ids: list[int]
