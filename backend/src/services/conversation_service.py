"""Conversation and message service."""

from datetime import UTC, datetime

from sqlmodel import Session, select

from src.models.conversation import Conversation
from src.models.message import Message, MessageRole


class ConversationService:
    """Service for conversation and message operations."""

    def __init__(self, session: Session):
        self.session = session

    def create_conversation(self, user_id: str) -> Conversation:
        """Create a new conversation for the user."""
        conversation = Conversation(user_id=user_id)
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def get_conversation(
        self, user_id: str, conversation_id: int
    ) -> Conversation | None:
        """Get a specific conversation by ID for a user."""
        statement = select(Conversation).where(
            Conversation.user_id == user_id,
            Conversation.id == conversation_id,
        )
        return self.session.exec(statement).first()

    def get_conversations(self, user_id: str) -> list[Conversation]:
        """Get all conversations for a user, ordered by most recent."""
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        )
        return list(self.session.exec(statement).all())

    def get_or_create_conversation(
        self, user_id: str, conversation_id: int | None = None
    ) -> Conversation:
        """Get existing conversation or create a new one."""
        if conversation_id:
            conversation = self.get_conversation(user_id, conversation_id)
            if conversation:
                return conversation
        return self.create_conversation(user_id)

    def add_message(
        self, conversation_id: int, role: MessageRole, content: str
    ) -> Message:
        """Add a message to a conversation."""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        self.session.add(message)

        # Update conversation's updated_at
        conversation = self.session.get(Conversation, conversation_id)
        if conversation:
            conversation.updated_at = datetime.now(UTC)
            self.session.add(conversation)

        self.session.commit()
        self.session.refresh(message)
        return message

    def get_messages(self, conversation_id: int) -> list[Message]:
        """Get all messages in a conversation, ordered chronologically."""
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        return list(self.session.exec(statement).all())

    def get_message_count(self, conversation_id: int) -> int:
        """Get the number of messages in a conversation."""
        statement = select(Message).where(Message.conversation_id == conversation_id)
        return len(list(self.session.exec(statement).all()))

    def get_last_message(self, conversation_id: int) -> Message | None:
        """Get the most recent message in a conversation."""
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(1)
        )
        return self.session.exec(statement).first()
