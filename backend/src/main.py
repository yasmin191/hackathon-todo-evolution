"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.database import create_db_and_tables
from src.routers import (
    blueprints_router,
    chat_router,
    reminders_router,
    skills_router,
    tags_router,
    tasks_router,
    voice_router,
)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    create_db_and_tables()
    yield


app = FastAPI(
    title="Todo API",
    description="Phase V - Cloud-Native AI-Powered Todo Application",
    version="0.5.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks_router)
app.include_router(tags_router)
app.include_router(chat_router)
app.include_router(reminders_router)
app.include_router(skills_router)
app.include_router(blueprints_router)
app.include_router(voice_router)


@app.get("/health")
def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}
