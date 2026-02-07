"""API routers."""

from src.routers.chat import router as chat_router
from src.routers.reminders import router as reminders_router
from src.routers.tags import router as tags_router
from src.routers.tasks import router as tasks_router

__all__ = ["tasks_router", "chat_router", "tags_router", "reminders_router"]
