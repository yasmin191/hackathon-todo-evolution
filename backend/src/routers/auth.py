"""Demo authentication endpoint for hackathon."""

import re
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter
from jose import jwt
from pydantic import BaseModel

from src.config import get_settings

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


class LoginRequest(BaseModel):
    """Demo login request."""

    email: str


class LoginResponse(BaseModel):
    """Demo login response with signed JWT."""

    user_id: str
    email: str
    token: str


@router.post("/demo-login", response_model=LoginResponse)
def demo_login(data: LoginRequest) -> LoginResponse:
    """Issue a properly signed JWT for demo/hackathon purposes."""
    user_id = "user_" + re.sub(r"[^a-zA-Z0-9]", "_", data.email)

    payload = {
        "sub": user_id,
        "email": data.email,
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
    }
    token = jwt.encode(payload, settings.better_auth_secret, algorithm="HS256")

    return LoginResponse(user_id=user_id, email=data.email, token=token)
