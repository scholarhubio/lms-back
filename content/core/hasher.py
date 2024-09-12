from core import settings
from faker import Faker
import random as rd
from interfaces.hasher import IHasher
from passlib.context import CryptContext


fake = Faker()


class DataHasher(IHasher):
    pwd_context = CryptContext(schemes=[settings.hasher.algorithm], deprecated="auto")

    async def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    async def random_password(self):
        choices = [
            f"{fake.last_name()}{fake.first_name()}",
            rd.randint(-1000000000, 100000000)]
        return rd.choice(choices)


async def get_data_hasher() -> DataHasher:
    return DataHasher()
