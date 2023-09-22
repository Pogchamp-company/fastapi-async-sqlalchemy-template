from typing import Any, Dict, List, Optional, Union

from pydantic import field_validator, AnyHttpUrl, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = 'ProjectName'
    HOST: str = '127.0.0.1'
    PORT: int = 8000
    DEBUG: bool = False
    LOGGER_NAME: str = 'main-logger'

    @field_validator('DEBUG', mode="before")
    @classmethod
    def assemble_bool(cls, v: Union[str, bool, None]) -> bool:
        return bool(v)

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator('BACKEND_CORS_ORIGINS', mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: Optional[str] = 'localhost:5432'
    POSTGRES_USER: Optional[str] = 'postgres'
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = 'db_name'
    DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator('DATABASE_URI', mode='before')
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if isinstance(v, str):
            return v

        params = dict(scheme='postgresql+asyncpg',
                      user=values.get('POSTGRES_USER'),
                      password=values.get('POSTGRES_PASSWORD'),
                      host=values.get('POSTGRES_SERVER'),
                      path=f"/{values.get('POSTGRES_DB')}"
                      )
        return PostgresDsn.build(**params)
    model_config = SettingsConfigDict(case_sensitive=True, env_file='.env')


settings = Settings()
