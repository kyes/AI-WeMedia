"""Tests for auth endpoints."""
from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.core.security import hash_password


async def _create_loginable_user(db: AsyncSession, email: str, password: str) -> User:
    """Create a user that can be logged in (committed to DB for login to work)."""
    user = User(
        email=email,
        username=email.split("@")[0].replace(".", "_"),
        hashed_password=hash_password(password),
        full_name="Test User",
    )
    db.add(user)
    await db.flush()
    return user


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    resp = await client.post("/api/v1/auth/register", json={
        "email": "brand_new@example.com",
        "username": "brandnewuser",
        "password": "secret123",
        "full_name": "New User",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "brand_new@example.com"
    assert data["username"] == "brandnewuser"
    assert "id" in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, db: AsyncSession):
    # Register once inside this test
    await _create_loginable_user(db, "dup_test@example.com", "password123")
    resp = await client.post("/api/v1/auth/register", json={
        "email": "dup_test@example.com",
        "username": "another_unique_user",
        "password": "password123",
    })
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, db: AsyncSession):
    await _create_loginable_user(db, "login_ok@example.com", "password123")
    resp = await client.post("/api/v1/auth/login", json={
        "email": "login_ok@example.com",
        "password": "password123",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, db: AsyncSession):
    await _create_loginable_user(db, "wrongpw@example.com", "correctpass")
    resp = await client.post("/api/v1/auth/login", json={
        "email": "wrongpw@example.com",
        "password": "wrongpassword",
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, auth_headers):
    resp = await client.get("/api/v1/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "fixture_user@example.com"


@pytest.mark.asyncio
async def test_get_me_unauthorized(client: AsyncClient):
    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient, db: AsyncSession):
    await _create_loginable_user(db, "refresh_user@example.com", "password123")
    login_resp = await client.post("/api/v1/auth/login", json={
        "email": "refresh_user@example.com",
        "password": "password123",
    })
    assert login_resp.status_code == 200
    refresh_token = login_resp.json()["refresh_token"]

    resp = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200
    assert resp.json()["access_token"]


@pytest.mark.asyncio
async def test_change_password(client: AsyncClient, auth_headers):
    resp = await client.post("/api/v1/auth/change-password", json={
        "current_password": "password123",
        "new_password": "newpassword456",
    }, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["message"] == "密码修改成功"


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
