from typing import Generator

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings


# @pytest.fixture(scope="session")
def setup_db() -> Generator:
    engine = create_engine(f"{settings.DATABASE_URI.replace('+asyncpg', '')}")
    conn = engine.connect()
    # トランザクションを一度終了させる
    conn.execute(text("commit"))
    try:
        conn.execute(text("drop database test"))
    except SQLAlchemyError:
        pass
    finally:
        conn.close()

    conn = engine.connect()
    # トランザクションを一度終了させる
    conn.execute(text("commit"))
    conn.execute(text("create database test"))
    conn.close()

    yield

    conn = engine.connect()
    # トランザクションを一度終了させる
    conn.execute(text("commit"))
    try:
        conn.execute(text("drop database test"))
    except SQLAlchemyError:
        pass
    conn.close()


pytest_plugins = [
    "tests.fixtures",
]
