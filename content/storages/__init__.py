from abc import ABC, abstractmethod


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

    @abstractmethod
    async def get_from_cashe(self, url: str):
        pass
