import sys
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator
from sqlalchemy.util import classproperty


class Settings(BaseSettings):
    PROJECT_NAME: str = 'ProjectName'
    HOST: str = '127.0.0.1'
    PORT: int = 8000
    DEBUG: bool = False
    LOGGER_NAME: str = 'main-logger'

    @validator('DEBUG', pre=True)
    def assemble_bool(cls, v: Union[str, bool, None]) -> bool:
        return bool(v)

    @classproperty
    def TESTING(self) -> bool:
        return 'pytest' in sys.modules

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator('BACKEND_CORS_ORIGINS', pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: Optional[str] = 'localhost:5432'
    POSTGRES_USER: Optional[str] = 'postgres'
    POSTGRES_PASSWORD: Optional[str]
    POSTGRES_DB: Optional[str] = 'db_name'
    DATABASE_URI: Optional[PostgresDsn] = None

    @validator('DATABASE_URI', pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if isinstance(v, str):
            if cls.TESTING:
                path_start = v.rfind('/') + 1
                v = v[:path_start] + 'test_' + v[path_start:]
            return v

        params = dict(scheme='postgresql+asyncpg',
                      user=values.get('POSTGRES_USER'),
                      password=values.get('POSTGRES_PASSWORD'),
                      host=values.get('POSTGRES_SERVER'),
                      path=f"/{values.get('POSTGRES_DB')}"
                      )

        if cls.TESTING:
            params.update(path=f"/test_{values.get('POSTGRES_DB')}")

        return PostgresDsn.build(**params)

    class Config:
        case_sensitive = True
        env_file = '.env'


settings = Settings()
