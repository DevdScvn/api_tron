import os
import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from core.models import db_helper
from core.models.base import Base
from main import main_app

os.environ["MODE"] = "TEST"

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session")
async def session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with SessionLocal() as session:

        def override_get_db():
            return session

        main_app.dependency_overrides[db_helper.session_getter] = override_get_db
        yield session


@pytest.fixture(scope="session")
async def ac():
    """Create an AsyncClient instance."""
    async with AsyncClient(transport=ASGITransport(app=main_app), base_url="https://test") as ac:
        yield ac
