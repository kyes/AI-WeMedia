"""Test configuration and fixtures."""
from __future__ import annotations

import asyncio
import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Must be set before any app imports so database.py picks it up
os.environ.setdefault("TEST_DATABASE_URL", "sqlite+aiosqlite:///./test.db")
os.environ.setdefault("APP_ENV", "testing")

from app.database import Base, get_db  # noqa: E402
from app.main import create_app  # noqa: E402
from app.models import User  # noqa: E402
from app.core.security import hash_password  # noqa: E402

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_tables():
    """Create all tables once per test session."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    """Each test gets its own session that is rolled back after."""
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    app = create_app()

    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def test_user(db: AsyncSession) -> User:
    """Create a test user within the current test session."""
    user = User(
        email="fixture_user@example.com",
        username="fixture_user",
        hashed_password=hash_password("password123"),
        full_name="Fixture User",
    )
    db.add(user)
    await db.flush()  # flush but NOT commit — rollback cleans up
    return user


@pytest_asyncio.fixture
async def auth_headers(client: AsyncClient, test_user: User, db: AsyncSession) -> dict[str, str]:
    """Get auth headers. Login directly via service to avoid DB commit issues."""
    from app.core.security import create_access_token
    access_token, _ = create_access_token(subject=test_user.id)
    return {"Authorization": f"Bearer {access_token}"}
