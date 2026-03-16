from arq.connections import ArqRedis, create_pool
from redis.asyncio import ConnectionPool, Redis

from src.config import settings

_pool: ConnectionPool | None = None


async def get_redis() -> Redis:
    global _pool
    if _pool is None:
        _pool = ConnectionPool.from_url(settings.redis_url)
    return Redis(connection_pool=_pool)


async def get_arq_redis() -> ArqRedis:
    return await create_pool(settings.redis_url)  # type: ignore[arg-type]
