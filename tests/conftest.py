from datetime import datetime, timezone

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from src.app import app
from src.ext.database.db import get_async_session
from src.resources import Base
from src.resources.events.model import Event
from src.resources.speakers.model import Speaker
from src.resources.talks.model import Talk
from src.resources.users.model import User

# Test database configuration
POSTGRES_IMAGE = 'postgres:17'
POSTGRES_USER = 'test_user'
POSTGRES_PASSWORD = 'test_password'
POSTGRES_DB = 'test_db'


@pytest.fixture(scope='session')
def postgres_container():
    """Start the Postgres test container."""
    container = PostgresContainer(
        POSTGRES_IMAGE, username=POSTGRES_USER, password=POSTGRES_PASSWORD, dbname=POSTGRES_DB, driver='asyncpg'
    )
    container.start()
    yield container
    container.stop()


@pytest.fixture(scope='module')
async def engine(postgres_container):
    """Create a test database engine with proper cleanup."""
    engine = create_async_engine(
        postgres_container.get_connection_url(),
        echo=True,
        future=True,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )
    return engine


@pytest.fixture(autouse=True)
async def setup_database(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    engine.dispose()


@pytest.fixture
async def session(engine):
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
        yield session

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as async_client:
        app.dependency_overrides[get_async_session] = get_override_session
        yield async_client
    app.dependency_overrides.clear()


@pytest.fixture
async def create_user(session):
    user_data = {
        'username': 'bento',
        'email': 'bento@test.com',
        'hashed_password': 'an!RW9j7654321',
    }
    user = User(**user_data)
    session.add(user)
    await session.commit()
    return user


@pytest.fixture
async def create_event(session):
    event_data = {
        'edition': 1,
        'title': 'Event 1',
        'description': 'Description 1',
        'start_date': datetime(2021, 1, 1, 7, 0, 0, tzinfo=timezone.utc),
        'end_date': datetime(2021, 1, 1, 9, 45, 0, tzinfo=timezone.utc),
        'location': 'Location 1',
        'image_url': 'https://example.com/image.jpg',
    }
    event = Event(**event_data)
    session.add(event)

    await session.commit()
    return event


@pytest.fixture
async def create_speaker(session):
    speaker_data = {
        'name': 'Speaker 1',
        'email': 'speaker1@test.com',
        'linkedin_url': 'https://linkedin.com/in/speaker1',
        'github_url': 'https://github.com/speaker1',
        'twitter_url': 'https://twitter.com/speaker1',
        'website_url': 'https://speaker1.com',
        'bio': 'Speaker 1 bio',
        'image_url': 'https://example.com/image.jpg',
    }
    speaker = Speaker(**speaker_data)
    session.add(speaker)
    await session.commit()
    return speaker


@pytest.fixture
async def create_talk(session, create_event, create_speaker):
    talk_data = {
        'title': 'Talk 1',
        'description': 'Description 1',
        'speaker_id': create_speaker.id,
        'start_time': datetime(2021, 1, 1, 7, 0, 0, tzinfo=timezone.utc),
        'end_time': datetime(2021, 1, 1, 9, 45, 0, tzinfo=timezone.utc),
        'event_id': create_event.id,
    }
    talk = Talk(**talk_data)
    session.add(talk)
    await session.commit()
    return talk
