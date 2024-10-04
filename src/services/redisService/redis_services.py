from redis import Redis


class RedisService:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    def get_by_key(self, key: str) -> str:
        return self._redis.get(key)

    def set_key_value(self, key: str, value: str) -> None:
        self._redis.set(key, value, ex=30)
