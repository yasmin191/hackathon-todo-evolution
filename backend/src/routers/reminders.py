"""Reminder API endpoints for Dapr cron binding."""

import logging

from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.database import get_session
from src.services import event_service
from src.services.task_service import TaskService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reminders", tags=["reminders"])


@router.post("/check")
async def check_reminders(db: Session = Depends(get_session)) -> dict:
    """Check for tasks needing reminders.

    This endpoint is called by Dapr cron binding every 5 minutes.
    It finds tasks with reminder_at <= now that haven't been reminded yet,
    publishes reminder events, and marks them as reminded.
    """
    service = TaskService(db)
    tasks = service.get_tasks_needing_reminder()

    reminded_count = 0
    for task in tasks:
        try:
            # Publish reminder event
            success = await event_service.publish_reminder(
                user_id=task.user_id,
                task_id=task.id,
                title=task.title,
                due_date=task.due_date.isoformat() if task.due_date else "",
            )

            if success:
                # Mark as reminded
                service.mark_reminded(task.id)
                reminded_count += 1
                logger.info(f"Sent reminder for task {task.id}: {task.title}")
        except Exception as e:
            logger.error(f"Failed to process reminder for task {task.id}: {e}")

    return {
        "checked": len(tasks),
        "reminded": reminded_count,
    }
