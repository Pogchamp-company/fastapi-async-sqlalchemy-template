from typing import Generator, AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy import create_engine, event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import Session, SessionTransaction

from app.core.config import settings
from app.database import BaseModel, get_session
from manage import app


@pytest.fixture(scope="session", autouse=True)
def setup_test_db() -> Generator:
    engine = create_engine(settings.DATABASE_URI.replace('+asyncpg', ''))

    with engine.begin():
        BaseModel.metadata.drop_all(engine)
        BaseModel.metadata.create_all(engine)
        yield
        BaseModel.metadata.drop_all(engine)


@pytest_asyncio.fixture(autouse=True)
async def session() -> AsyncGenerator:
    # https://github.com/sqlalchemy/sqlalchemy/issues/5811#issuecomment-756269881
    async_engine = create_async_engine(settings.DATABASE_URI)
    async with async_engine.connect() as conn:
        await conn.begin()
        await conn.begin_nested()
        async_session_factory = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=conn,
        )

        async_session = async_session_factory()

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(_session: Session, _transaction: SessionTransaction) -> None:
            if conn.closed:
                return
            if not conn.in_nested_transaction():
                if conn.sync_connection:
                    conn.sync_connection.begin_nested()

        def test_get_session() -> Generator:
            try:
                yield async_session_factory()
            except SQLAlchemyError:
                pass

        app.dependency_overrides[get_session] = test_get_session

        yield async_session
        await async_session.close()
        await conn.rollback()
