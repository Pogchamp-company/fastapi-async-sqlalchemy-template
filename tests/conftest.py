from app.core.config import settings


def override_db_name():
    """Prefix database name with test_"""
    uri = settings.DATABASE_URI
    path_start = uri.rfind('/') + 1
    uri = uri[:path_start] + 'test_' + uri[path_start:]
    settings.DATABASE_URI = uri


override_db_name()

pytest_plugins = [
    "tests.fixtures",
]
