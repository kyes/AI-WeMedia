"""Security utilities: JWT tokens, password hashing."""
from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ─── Password helpers ────────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ─── JWT helpers ─────────────────────────────────────────────────────────────

def create_access_token(subject: str, extra: dict | None = None) -> tuple[str, int]:
    """Return (token, expires_in_seconds)."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )
    payload: dict = {"sub": subject, "exp": expire, "type": "access"}
    if extra:
        payload.update(extra)
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token, settings.jwt_access_token_expire_minutes * 60


def create_refresh_token() -> tuple[str, str, datetime]:
    """Return (plain_token, token_hash, expires_at)."""
    plain = secrets.token_urlsafe(48)
    token_hash = hashlib.sha256(plain.encode()).hexdigest()
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.jwt_refresh_token_expire_days)
    return plain, token_hash, expires_at


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT; raises JWTError on failure."""
    payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    if payload.get("type") != "access":
        raise JWTError("invalid token type")
    return payload


def hash_token(plain: str) -> str:
    return hashlib.sha256(plain.encode()).hexdigest()
