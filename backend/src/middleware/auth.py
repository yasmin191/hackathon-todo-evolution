"""JWT authentication middleware."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from src.config import get_settings

settings = get_settings()
security = HTTPBearer()


class AuthUser:
    """Authenticated user extracted from JWT token."""

    def __init__(self, user_id: str, email: str | None = None):
        self.user_id = user_id
        self.email = email


def decode_token(token: str) -> dict:
    """Decode and verify JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=["HS256"],
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> AuthUser:
    """Extract and verify user from JWT token."""
    payload = decode_token(credentials.credentials)

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return AuthUser(
        user_id=user_id,
        email=payload.get("email"),
    )


def verify_user_access(path_user_id: str, current_user: AuthUser) -> None:
    """Verify the authenticated user can access the requested resource.

    Returns 404 instead of 403 to prevent user enumeration.
    """
    if path_user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found",
        )


CurrentUser = Annotated[AuthUser, Depends(get_current_user)]
