from redis.asyncio import Redis
from fastapi import Depends
from storages import ICasheClient


redis: Redis | None = None


class Client(ICasheClient):
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
    
    async def setex(self, key: str, seconds: int, value: dict):
        await self.redis.setex(key, seconds, value)

    async def exists(self, key: str):
        return await self.redis.exists(key)
    
    async def save(self, key: str):
        return await super().save(key)
    
    async def delete(self, key: str):
        return await super().delete(key)
    
    async def get_from_cashe(self, key: str):
        return await self.redis.getex(key)


async def get_redis():
    return redis


async def get_redis_client(redis: Redis = Depends(get_redis)):
    return Client(redis)
