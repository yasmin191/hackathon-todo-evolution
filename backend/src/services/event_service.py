"""Event publishing service using Dapr pub/sub."""

import logging
import os
from datetime import UTC, datetime
from typing import Any

import httpx

logger = logging.getLogger(__name__)

DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
PUBSUB_NAME = "task-pubsub"
DAPR_ENABLED = os.getenv("DAPR_ENABLED", "false").lower() == "true"


async def publish_event(
    topic: str,
    event_type: str,
    user_id: str,
    task_id: int | None = None,
    data: dict[str, Any] | None = None,
) -> bool:
    """Publish an event to a Dapr pub/sub topic.

    Args:
        topic: The topic to publish to (e.g., "task-events")
        event_type: Type of event (e.g., "task.created", "task.completed")
        user_id: The user ID associated with the event
        task_id: Optional task ID
        data: Additional event data

    Returns:
        True if published successfully, False otherwise
    """
    if not DAPR_ENABLED:
        logger.debug(f"Dapr disabled, skipping event: {event_type}")
        return False

    event = {
        "id": f"{event_type}-{task_id or 'none'}-{datetime.now(UTC).timestamp()}",
        "source": "todo-backend",
        "type": event_type,
        "specversion": "1.0",
        "datacontenttype": "application/json",
        "data": {
            "event_type": event_type,
            "user_id": user_id,
            "task_id": task_id,
            "timestamp": datetime.now(UTC).isoformat(),
            **(data or {}),
        },
    }

    url = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/{PUBSUB_NAME}/{topic}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=event,
                headers={"Content-Type": "application/cloudevents+json"},
                timeout=5.0,
            )
            response.raise_for_status()
            logger.info(f"Published event {event_type} to {topic}")
            return True
    except httpx.HTTPError as e:
        logger.warning(f"Failed to publish event {event_type}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error publishing event: {e}")
        return False


async def publish_task_created(user_id: str, task_id: int, title: str) -> bool:
    """Publish a task.created event."""
    return await publish_event(
        topic="task-events",
        event_type="task.created",
        user_id=user_id,
        task_id=task_id,
        data={"title": title},
    )


async def publish_task_updated(user_id: str, task_id: int, changes: dict) -> bool:
    """Publish a task.updated event."""
    return await publish_event(
        topic="task-events",
        event_type="task.updated",
        user_id=user_id,
        task_id=task_id,
        data={"changes": changes},
    )


async def publish_task_completed(user_id: str, task_id: int, title: str) -> bool:
    """Publish a task.completed event."""
    return await publish_event(
        topic="task-completed",
        event_type="task.completed",
        user_id=user_id,
        task_id=task_id,
        data={"title": title},
    )


async def publish_task_deleted(user_id: str, task_id: int, title: str) -> bool:
    """Publish a task.deleted event."""
    return await publish_event(
        topic="task-events",
        event_type="task.deleted",
        user_id=user_id,
        task_id=task_id,
        data={"title": title},
    )


async def publish_reminder(
    user_id: str, task_id: int, title: str, due_date: str
) -> bool:
    """Publish a reminder event."""
    return await publish_event(
        topic="task-reminders",
        event_type="reminder.due",
        user_id=user_id,
        task_id=task_id,
        data={"title": title, "due_date": due_date},
    )
