"""Message model for chat messages."""

from datetime import UTC, datetime
from enum import Enum

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(UTC)


class MessageRole(str, Enum):
    """Message role enum."""

    USER = "user"
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    """Message database model for chat messages."""

    __tablename__ = "messages"

    id: int | None = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: MessageRole
    content: str
    created_at: datetime = Field(default_factory=utc_now)


class MessageCreate(SQLModel):
    """Schema for creating a message."""

    role: MessageRole
    content: str


class MessageResponse(SQLModel):
    """Schema for message API responses."""

    id: int
    conversation_id: int
    role: MessageRole
    content: str
    created_at: datetime
