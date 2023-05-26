import re

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import as_declarative, declared_attr

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URI, echo=False, pool_pre_ping=True)
async_session = async_sessionmaker(
    engine, expire_on_commit=False, autocommit=False, autoflush=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


@as_declarative(metadata=metadata)
class BaseModel:

    @declared_attr
    def __tablename__(cls) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()

    def __repr__(self) -> str:
        pk = inspect(self.__class__).primary_key[0].name
        return f'<{self.__class__.__name__} {getattr(self, pk, id(self))}>'
