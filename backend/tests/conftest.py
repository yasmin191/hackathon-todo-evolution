"""Test configuration and fixtures."""

import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

# Set test environment variables before importing app
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["BETTER_AUTH_SECRET"] = "test-secret-key-for-jwt-tokens-min-32"
os.environ["CORS_ORIGINS"] = "http://localhost:3000"

from src.database import get_session

from src.main import app


@pytest.fixture(name="engine")
def engine_fixture():
    """Create a test database engine."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(engine) -> Generator[Session, None, None]:
    """Provide a test database session."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    """Provide a test client with overridden session."""

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="auth_headers")
def auth_headers_fixture() -> dict[str, str]:
    """Provide authentication headers with a valid JWT token."""
    token = jwt.encode(
        {"sub": "test-user-123", "email": "test@example.com"},
        os.environ["BETTER_AUTH_SECRET"],
        algorithm="HS256",
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(name="other_user_headers")
def other_user_headers_fixture() -> dict[str, str]:
    """Provide authentication headers for a different user."""
    token = jwt.encode(
        {"sub": "other-user-456", "email": "other@example.com"},
        os.environ["BETTER_AUTH_SECRET"],
        algorithm="HS256",
    )
    return {"Authorization": f"Bearer {token}"}
