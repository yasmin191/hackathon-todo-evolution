"""API routers."""

from src.routers.auth import router as auth_router
from src.routers.blueprints import router as blueprints_router
from src.routers.chat import router as chat_router
from src.routers.reminders import router as reminders_router
from src.routers.skills import router as skills_router
from src.routers.tags import router as tags_router
from src.routers.tasks import router as tasks_router
from src.routers.voice import router as voice_router

__all__ = [
    "auth_router",
    "tasks_router",
    "chat_router",
    "tags_router",
    "reminders_router",
    "skills_router",
    "blueprints_router",
    "voice_router",
]
