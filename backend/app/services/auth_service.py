"""Authentication & User management service."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError, UnauthorizedError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_token,
    verify_password,
)
from app.models import RefreshToken, User
from app.schemas import TokenResponse, UserLogin, UserRegister


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def register(self, data: UserRegister) -> User:
        """Register a new user, raise ConflictError if email/username taken."""
        # Check uniqueness
        existing = await self.db.execute(
            select(User).where(
                (User.email == data.email) | (User.username == data.username)
            )
        )
        if existing.scalar_one_or_none():
            raise ConflictError("Email or username already registered")

        user = User(
            email=data.email,
            username=data.username,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
        )
        self.db.add(user)
        await self.db.flush()
        return user

    async def login(self, data: UserLogin) -> TokenResponse:
        """Authenticate and return JWT token pair."""
        result = await self.db.execute(select(User).where(User.email == data.email))
        user = result.scalar_one_or_none()
        if not user or not verify_password(data.password, user.hashed_password):
            raise UnauthorizedError("Invalid credentials")
        if not user.is_active:
            raise UnauthorizedError("Account is disabled")

        access_token, expires_in = create_access_token(subject=user.id)
        plain_refresh, token_hash, expires_at = create_refresh_token()

        rt = RefreshToken(user_id=user.id, token_hash=token_hash, expires_at=expires_at)
        self.db.add(rt)

        user.last_login_at = datetime.now(timezone.utc)
        await self.db.flush()

        return TokenResponse(
            access_token=access_token,
            refresh_token=plain_refresh,
            expires_in=expires_in,
        )

    async def refresh(self, plain_refresh_token: str) -> TokenResponse:
        """Rotate refresh token and return a new token pair."""
        token_hash = hash_token(plain_refresh_token)
        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash == token_hash,
                RefreshToken.revoked == False,  # noqa: E712
            )
        )
        rt = result.scalar_one_or_none()
        now = datetime.now(timezone.utc)
        # Normalize to aware for SQLite which stores naive datetimes
        expires = rt.expires_at if rt.expires_at.tzinfo else rt.expires_at.replace(tzinfo=timezone.utc)
        if rt is None or expires < now:
            raise UnauthorizedError("Invalid or expired refresh token")

        # Revoke old token
        rt.revoked = True

        user_result = await self.db.execute(select(User).where(User.id == rt.user_id))
        user = user_result.scalar_one_or_none()
        if not user or not user.is_active:
            raise UnauthorizedError("User not found")

        access_token, expires_in = create_access_token(subject=user.id)
        plain_new, new_hash, new_expires = create_refresh_token()
        new_rt = RefreshToken(user_id=user.id, token_hash=new_hash, expires_at=new_expires)
        self.db.add(new_rt)
        await self.db.flush()

        return TokenResponse(
            access_token=access_token,
            refresh_token=plain_new,
            expires_in=expires_in,
        )

    async def get_user_by_id(self, user_id: str) -> User:
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("User not found")
        return user
