import logging

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from app.core.config import settings
from app.database import get_session, BaseModel


class BaseAuthorize:
    session: AsyncSession = Depends(get_session)

    def __init__(self):
        self.logger: logging.Logger = logging.getLogger(settings.LOGGER_NAME)

    async def _get_obj(self, q: Select) -> BaseModel | None:
        request = await self.session.execute(q)
        return o[0] if (o := request.unique().one_or_none()) else o
