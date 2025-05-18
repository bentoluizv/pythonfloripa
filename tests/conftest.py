import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from src.app import app
from src.ext.database.db import Base, get_async_session

# Test database configuration
POSTGRES_IMAGE = 'postgres:17'
POSTGRES_USER = 'test_user'
POSTGRES_PASSWORD = 'test_password'
POSTGRES_DB = 'test_db'


@pytest.fixture(scope='module')
async def engine():
    """Create a test database engine with proper cleanup."""
    with PostgresContainer(driver='asyncpg') as container:
        _engine = create_async_engine(
            container.get_connection_url(),
            echo=True,
            future=True,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
        async with _engine.begin():
            yield _engine


@pytest.fixture
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        async_session_maker = async_sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
        )
        async with async_session_maker() as session:
            yield session
            await session.rollback()


@pytest.fixture
async def client(session):
    """Create an async client for testing."""

    async def get_override_session():
        return session

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as async_client:
        app.dependency_overrides[get_async_session] = get_override_session
        yield async_client
    app.dependency_overrides.clear()
