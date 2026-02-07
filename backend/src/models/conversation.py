"""Conversation model for chat sessions."""

from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(UTC)


class Conversation(SQLModel, table=True):
    """Conversation database model for chat sessions."""

    __tablename__ = "conversations"

    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class ConversationResponse(SQLModel):
    """Schema for conversation API responses."""

    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0
    last_message: str | None = None
