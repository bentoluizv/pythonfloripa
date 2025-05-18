import pytest
from sqlalchemy import text

from src.ext.database.db import Base


@pytest.mark.asyncio
async def test_database_engine(metadata_test_engine):
    engine = await anext(metadata_test_engine)
    assert engine.dialect.name == 'postgresql'
    assert engine.dialect.driver == 'asyncpg'

    async with engine.begin() as conn:
        # Check tables before creation
        result = await conn.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        )
        tables_before = [row[0] for row in result]
        assert len(tables_before) == 0, 'Tables already exist in the database'

        # Create tables from metadata
        await conn.run_sync(Base.metadata.create_all)

        # Check tables after creation
        result = await conn.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        )
        tables_after = [row[0] for row in result]

        # Verify that tables were created only if they exist in metadata
        if Base.metadata.tables:
            assert len(tables_after) > len(tables_before), 'No tables were created from metadata'
            for table_name in Base.metadata.tables.keys():
                assert table_name in tables_after, f'Table {table_name} was not created'
        else:
            assert len(tables_after) == len(tables_before), 'Tables were created even though metadata is empty'

        # Clean up - drop all tables
        await conn.run_sync(Base.metadata.drop_all)

        # Verify cleanup
        result = await conn.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        )
        tables_after_cleanup = [row[0] for row in result]
        assert len(tables_after_cleanup) == 0, 'Tables were not properly cleaned up'


@pytest.mark.asyncio
async def test_database_session(session):
    session = await anext(session)
    assert session is not None
    async with session.begin() as conn:
        assert conn.is_active
