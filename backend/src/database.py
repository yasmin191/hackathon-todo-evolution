"""Database connection and session management."""

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from src.config import get_settings

settings = get_settings()

# Create engine with appropriate settings for the database type
_engine_kwargs = {
    "echo": False,
}

# Add connection pooling for PostgreSQL (not supported by SQLite)
if not settings.database_url.startswith("sqlite"):
    _engine_kwargs.update(
        {
            "pool_pre_ping": True,
            "pool_size": 5,
            "max_overflow": 10,
        }
    )

engine = create_engine(settings.database_url, **_engine_kwargs)


def create_db_and_tables() -> None:
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Provide a database session as a FastAPI dependency."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
