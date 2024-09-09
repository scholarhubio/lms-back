from models import User
from strategies.student import StudentQueryStrategy
from dal.postgres import PostgresDAL
from repositories.student import StudentRepository
from models.users.choices import RoleType
from repositories import IRoleRepository
from abc import ABC, abstractmethod
from schemas.user import UserSchema
from exceptions import NotEnoughPermission


class IRoleRepositoryFactory(ABC):

    @abstractmethod
    async def get_repository(self) -> IRoleRepository:
        pass


class RoleRepositoryFactory:
    """Factory to select the appropriate repository based on the user's role."""
    __repositories = {
        RoleType.STUDENT.value: StudentRepository(
             strategy=StudentQueryStrategy(),
             dal=PostgresDAL()
        ),
        RoleType.CEO.value: StudentRepository(
             strategy=StudentQueryStrategy(),
             dal=PostgresDAL()
        )
        }
    @classmethod
    async def get_repository(cls, user: UserSchema) -> IRoleRepository:
        """Select the correct repository based on the user's role."""
        repo = cls.__repositories.get(user.role, None)
        if repo:
            return repo
        else:
            raise NotEnoughPermission


async def get_role_repo_factory() -> IRoleRepositoryFactory:
    return RoleRepositoryFactory()
