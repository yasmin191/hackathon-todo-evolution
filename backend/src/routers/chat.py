"""Chat API endpoints."""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.agents import run_agent
from src.database import SessionDep
from src.middleware.auth import CurrentUser
from src.models.conversation import ConversationResponse
from src.models.message import MessageResponse, MessageRole
from src.services.conversation_service import ConversationService

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""

    message: str
    conversation_id: int | None = None


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""

    response: str
    conversation_id: int
    message_id: int


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    session: SessionDep,
    current_user: CurrentUser,
) -> ChatResponse:
    """Process a chat message and return AI response.

    Creates a new conversation if conversation_id is not provided.
    Saves both user message and assistant response to database.
    """
    conv_service = ConversationService(session)

    # Get or create conversation
    conversation = conv_service.get_or_create_conversation(
        current_user.user_id,
        request.conversation_id,
    )

    # Save user message
    conv_service.add_message(
        conversation.id,
        MessageRole.USER,
        request.message,
    )

    # Get conversation history for context
    messages = conv_service.get_messages(conversation.id)
    history = [
        {"role": msg.role.value, "content": msg.content}
        for msg in messages[:-1]  # Exclude the just-added message
    ]

    # Run AI agent
    try:
        response_text = await run_agent(
            session=session,
            user_id=current_user.user_id,
            message=request.message,
            history=history if history else None,
        )
    except Exception as e:
        # Save error message and re-raise
        error_msg = "I'm sorry, I encountered an error processing your request. Please try again."
        conv_service.add_message(
            conversation.id,
            MessageRole.ASSISTANT,
            error_msg,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e

    # Save assistant response
    assistant_message = conv_service.add_message(
        conversation.id,
        MessageRole.ASSISTANT,
        response_text,
    )

    return ChatResponse(
        response=response_text,
        conversation_id=conversation.id,
        message_id=assistant_message.id,
    )


@router.get("/conversations", response_model=list[ConversationResponse])
def list_conversations(
    session: SessionDep,
    current_user: CurrentUser,
) -> list[ConversationResponse]:
    """Get all conversations for the current user."""
    conv_service = ConversationService(session)
    conversations = conv_service.get_conversations(current_user.user_id)

    result = []
    for conv in conversations:
        message_count = conv_service.get_message_count(conv.id)
        last_msg = conv_service.get_last_message(conv.id)

        result.append(
            ConversationResponse(
                id=conv.id,
                user_id=conv.user_id,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
                message_count=message_count,
                last_message=last_msg.content[:100] if last_msg else None,
            )
        )

    return result


@router.get(
    "/conversations/{conversation_id}/messages", response_model=list[MessageResponse]
)
def get_conversation_messages(
    conversation_id: int,
    session: SessionDep,
    current_user: CurrentUser,
) -> list[MessageResponse]:
    """Get all messages in a conversation."""
    conv_service = ConversationService(session)

    # Verify user owns the conversation
    conversation = conv_service.get_conversation(
        current_user.user_id,
        conversation_id,
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    messages = conv_service.get_messages(conversation_id)
    return [
        MessageResponse(
            id=msg.id,
            conversation_id=msg.conversation_id,
            role=msg.role,
            content=msg.content,
            created_at=msg.created_at,
        )
        for msg in messages
    ]
