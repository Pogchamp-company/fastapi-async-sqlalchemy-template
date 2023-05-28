import logging
from app.core.config import settings


def get_default_logger() -> logging.Logger:
    return logging.getLogger(settings.LOGGER_NAME)
