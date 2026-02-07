"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.database import create_db_and_tables
from src.routers import tasks_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    create_db_and_tables()
    yield


app = FastAPI(
    title="Todo API",
    description="Phase II - Full-Stack Todo Application Backend",
    version="0.1.0",
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


@app.get("/health")
def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}
