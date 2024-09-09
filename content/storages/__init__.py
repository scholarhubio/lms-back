from abc import ABC, abstractmethod
from typing import Any

class ICasheClient(ABC):
    @abstractmethod
    async def save(self, key: str, ):
        pass

    @abstractmethod
    async def delete(self, key: str):
        pass
    
    @abstractmethod
    async def setex(self, key: str, seconds: int, value: dict):
        pass

    @abstractmethod
    async def exists(self, key: str):
        pass


class ICashe(ABC):
    def __init__(self, client: ICasheClient) -> None:
        self.client = client

    @abstractmethod
    async def get_from_cache(self, url: str):
        pass

    @abstractmethod
    async def put_to_cache(self, url: str, data: Any):
        pass

    async def set_exp(self, key: str, seconds: int, value: dict):
        return await self.set_exp(key, seconds, value)

    async def exists(self, key: str):
        return await self.client.exists(key)
