from app.settings import settings
from .base import AbstractCache
from .local import InMemoryCache
from .redis import RedisCache


def get_cache() -> AbstractCache:
    """
    Возвращает кэш в зависимости от настроек приложения.

    Если указана переменная окружения REDIS_HOST, то возвращает кэш в Redis.
    Если нет, то возвращает кэш в памяти.
    """
    if settings.REDIS_HOST:
        return RedisCache(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
        )
    else:
        return InMemoryCache()
