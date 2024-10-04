from typing import AsyncIterator

import redis


async def init_redis_pool(host: str, password: str, port: int) -> AsyncIterator[redis.Redis]:
    session = redis.Redis(
        host=host,
        port=port,
        password=password,
        ssl=True,
        db=0,
    )
    yield session
    session.close()
    await session.wait_closed()
