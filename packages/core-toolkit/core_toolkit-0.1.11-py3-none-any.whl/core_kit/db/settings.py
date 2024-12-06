import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool = False
    POOL_SIZE: int = 10
    MAX_OVERFLOW: int = 10
    PREPARED_STATEMENT_CACHE_SIZE: int = 100
    STATEMENT_CACHE_SIZE: int = 100
    model_config = SettingsConfigDict(
        env_file=os.environ.get("ENV_FILE_PATH", ".env"),
        extra="allow",
    )


settings = Settings()
