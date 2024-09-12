from typing import Any
from db.redis import get_redis_client
from . import ICashe
from fastapi import Depends


class Cashe(ICashe):    
    async def get_from_cache(self, url: str):
        return await super().get_from_cache(url)
    
    async def put_to_cache(self, url: str, data: Any):
        return await super().put_to_cache(url, data)


async def get_cashe(client=Depends(get_redis_client)):
    return Cashe(
        client=client
    )
