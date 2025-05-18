import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from src.app import app
from src.ext.database.db import Base

# Test database configuration
POSTGRES_IMAGE = 'postgres:17'
POSTGRES_USER = 'test_user'
POSTGRES_PASSWORD = 'test_password'
POSTGRES_DB = 'test_db'
METADATA_TEST_DB = 'metadata_test_db'


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(scope='session')
async def engine():
    """Create a test database engine with proper cleanup."""
    container = PostgresContainer(
        POSTGRES_IMAGE, username=POSTGRES_USER, password=POSTGRES_PASSWORD, dbname=POSTGRES_DB, driver='asyncpg'
    )

    try:
        container.start()
        TEST_DATABASE_URL = container.get_connection_url()

        engine = create_async_engine(
            TEST_DATABASE_URL,
            echo=True,
            future=True,
            pool_pre_ping=True,  # Enable connection health checks
            pool_size=5,  # Limit pool size for tests
            max_overflow=10,
        )

        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        yield engine

    except Exception as e:
        pytest.fail(f'Failed to setup test database: {str(e)}')
    finally:
        container.stop()


@pytest.fixture
async def metadata_test_engine():
    """Create a separate test database engine for metadata testing."""
    container = PostgresContainer(
        POSTGRES_IMAGE, username=POSTGRES_USER, password=POSTGRES_PASSWORD, dbname=METADATA_TEST_DB, driver='asyncpg'
    )

    try:
        container.start()
        TEST_DATABASE_URL = container.get_connection_url()

        engine = create_async_engine(
            TEST_DATABASE_URL,
            echo=True,
            future=True,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )

        yield engine

    except Exception as e:
        pytest.fail(f'Failed to setup metadata test database: {str(e)}')
    finally:
        container.stop()


@pytest.fixture
async def session(engine):
    """Create a test database session with automatic rollback."""
    async_engine = await anext(engine)

    async_session_maker = async_sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
    )

    async with async_session_maker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
