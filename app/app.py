import logging
import sys
from http import HTTPStatus

import json_logging
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from starlette.authentication import AuthenticationError
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

from app.core.config import settings
from app.utils.logs_formatters import JSONRequestLogFormatter, JSONLogWebFormatter


def get_application() -> FastAPI:
    override_422_docs()

    docs = {'docs_url': None, 'redoc_url': None, 'openapi_url': None} if not settings.DEBUG else {}
    _app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG, **docs)

    init_extensions(_app)
    init_middlewares(_app)
    init_routers(_app)
    init_errors_handlers(_app)

    return _app


def override_422_docs() -> None:
    from app.errors_handlers.schemas import ErrorResponse
    import fastapi.openapi.utils as fu
    fu.validation_error_response_definition = ErrorResponse.model_json_schema()


def init_extensions(app: FastAPI) -> None:
    json_logging.init_fastapi(enable_json=True, custom_formatter=JSONLogWebFormatter)
    json_logging.init_request_instrument(app, JSONRequestLogFormatter)

    # init the logger as usual
    logger = logging.getLogger(settings.LOGGER_NAME)
    logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
    logger.addHandler(logging.StreamHandler(sys.stdout))


def init_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        RawContextMiddleware,
        plugins=(
            plugins.RequestIdPlugin(),
            plugins.CorrelationIdPlugin()
        )
    )


def init_routers(app: FastAPI) -> None:
    from app.example.crud import example_crud_router

    @app.get('/ping')
    async def ping() -> dict[str, bool | str]:
        return {'ok': True, 'detail': 'pong'}

    app.include_router(example_crud_router)


def init_errors_handlers(app: FastAPI) -> None:
    from app.errors_handlers import (authentication_handler, db_error,
                                     internal_server_error_handler, validation_exception_handler)
    app.add_exception_handler(AuthenticationError, authentication_handler)
    app.add_exception_handler(SQLAlchemyError, db_error)
    app.add_exception_handler(HTTPStatus.INTERNAL_SERVER_ERROR, internal_server_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
