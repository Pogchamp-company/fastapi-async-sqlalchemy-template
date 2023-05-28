import logging

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.utils.get_logger import get_default_logger


class BaseCBV:
    session: AsyncSession = Depends(get_session)
    logger: logging.Logger = Depends(get_default_logger)
