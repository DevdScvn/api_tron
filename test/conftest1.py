import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy_utils.functions import (create_database, database_exists,
                                        drop_database)

from core.config import settings
from database.connection import get_session
from main import app
from models.wallet import Base

ASYNC_TEST_DB_URL = settings.postgres.postgres_url + '_test'
SYNC_TEST_DB_URL = ASYNC_TEST_DB_URL.replace('+asyncpg', '')


@pytest.fixture(scope='session')
def setup_test_db():
    '''Создание тестовой базы данных'''
    if not database_exists(SYNC_TEST_DB_URL):
        create_database(SYNC_TEST_DB_URL)
    yield
    if database_exists(SYNC_TEST_DB_URL):
        drop_database(SYNC_TEST_DB_URL)


@pytest_asyncio.fixture(name='session')
async def session_fixture(setup_test_db):
    '''Фикстура для сессии'''
    engine = create_async_engine(ASYNC_TEST_DB_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session = async_sessionmaker(engine, expire_on_commit=False)
    async with session() as s:
        yield s
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(name='client')
async def client_fixture(session: AsyncSession):
    '''Клиентская фикстура'''
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        yield client
    app.dependency_overrides.clear()


pytest_plugins = [
    'tests.fixtures.wallet'
]
