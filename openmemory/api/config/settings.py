from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: Literal['local', 'production'] = 'production'
    log_level: Literal['DEBUG', 'INFO', 'WARN', 'ERROR'] = 'WARN'
    database_url: Optional[str] = None
    schema_name: Optional[str] = None
    user_id: Optional[str] = None
    app_id: Optional[str] = None

    model_config = SettingsConfigDict(env_file=Path(__file__).parents[1].joinpath(".env"), extra='ignore')


@lru_cache
def get_settings():
    return Settings()
