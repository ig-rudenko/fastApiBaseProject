from pydantic_settings import BaseSettings


class _BaseSettings(BaseSettings):
    log_level: str = "INFO"

    database_url: str = ""  # Путь к базе данных

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_HOURS: int = 24 * 14

    # Redis cache
    REDIS_HOST: str = ""
    REDIS_PASSWORD: str | None = None
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0


settings: _BaseSettings = _BaseSettings()
