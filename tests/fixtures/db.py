import contextlib

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings
from app.database import BaseModel
from manage import app

engine = create_engine(settings.DATABASE_URI.replace('+asyncpg', ''), pool_pre_ping=True)
session_factory = sessionmaker(
    engine, expire_on_commit=False, autocommit=False, autoflush=False
)

BaseModel.metadata.create_all(bind=engine)


@app.on_event("shutdown")
async def shutdown():
    BaseModel.metadata.drop_all(bind=engine)


def clear_db():
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(BaseModel.metadata.sorted_tables):
            con.execute(table.delete())
        trans.commit()


@pytest.fixture
def session() -> Session:
    with session_factory() as session:
        yield session
    # clear_db()
