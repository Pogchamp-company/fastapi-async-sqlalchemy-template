import re

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URI, echo=False, pool_pre_ping=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@as_declarative()
class BaseModel:

    @declared_attr
    def __tablename__(cls) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()

    def __repr__(self) -> str:
        pk = inspect(self.__class__).primary_key[0].name
        return f'<{self.__class__.__name__} {getattr(self, pk, id(self))}>'
