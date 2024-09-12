from abc import ABC, abstractmethod

class IHasher(ABC):
    @abstractmethod
    async def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    async def verify_password(self, password: str, hashed_password: str) -> bool:
        pass

    @abstractmethod
    async def random_password(self) -> str:
        pass
