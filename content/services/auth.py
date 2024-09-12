from abc import ABC, abstractmethod

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials

from interfaces.storage import IUserStorage
from interfaces.hasher import IHasher

from models.users.choices import RoleType
from models.users import User
from storages.user import get_user_storage

from core.security import CustomHTTPBearer
from core.hasher import get_data_hasher

from schemas.auth import UserRegistration, UserLogin

from db.postgres import get_async_session
from db.redis import get_redis_client, ICasheClient

from sqlalchemy.ext.asyncio import AsyncSession
from async_fastapi_jwt_auth import AuthJWT
from datetime import datetime, timezone
from core.utils import async_json_dumps, async_json_loads


class IAuthenticationService(ABC):
    @abstractmethod
    async def register_user(self):
        pass

    @abstractmethod
    async def login_user(self):
        pass
    
    @abstractmethod
    async def logout_user(self):
        pass

    @abstractmethod
    async def refresh_access_token(self):
        pass

    @abstractmethod
    async def get_current_user(self):
        pass


class AuthenticationService:
    def __init__(
        self,
        user_storage: IUserStorage,
        hasher: IHasher,
        cache: ICasheClient,
        session: AsyncSession,
        Authorize: AuthJWT
    ):
        self.user_storage = user_storage
        self.hasher = hasher
        self.cache = cache
        self.session = session
        self.Authorize = Authorize

    async def register_user(self, user: UserRegistration):
        """Register a new user."""
        stored_user = await self.user_storage.get_user_by_phone(user.phone, session=self.session)
        if stored_user:
            raise HTTPException(status_code=400, detail="User already exists.")
        hashed_password = await self.hasher.hash_password(user.password)
        await self.user_storage.create_new_user(
            phone=user.phone, password=hashed_password,
            role=RoleType.STUDENT, session=self.session)
        return {"msg": "User registered successfully"}

    async def login_user(self, user: UserLogin):
        """Login the user and return access and refresh tokens."""
        stored_user = await self.user_storage.get_user_by_phone(user.phone, session=self.session)
        if not stored_user:
            raise HTTPException(status_code=400, detail="Invalid username or password.")

        is_verified = await self.hasher.verify_password(user.password, stored_user.password)
        if not is_verified:
            raise HTTPException(status_code=400, detail="Invalid username or password.")

        # Create a subject dict that includes user details
        subject = await async_json_dumps({"id": str(stored_user.id), "role": stored_user.role})

        # Generate access and refresh tokens with the customized subject
        access_token = await self.Authorize.create_access_token(subject=subject, user_claims={"type": "access"})
        refresh_token = await self.Authorize.create_refresh_token(subject=subject, user_claims={"type": "refresh"})
        return {"access_token": access_token, "refresh_token": refresh_token}

    async def logout_user(self):
        """Logout the user and add the access token to the denied list with expiration."""
        await self.Authorize.jwt_required()
        raw_jwt = await self.Authorize.get_raw_jwt()
        jti = raw_jwt["jti"]
        exp_timestamp = raw_jwt["exp"]
        current_timestamp = datetime.now(tz=timezone.utc).timestamp()
        expiration_time = int(exp_timestamp - current_timestamp)

        # Add the token to the denied list with expiration time
        await self.cache.setex(jti, seconds=expiration_time, value="true")
        print(jti, 'logout')
        return {"msg": "Successfully logged out"}

    async def refresh_access_token(self):
        """Refresh the access token using the refresh token."""
        await self.Authorize.jwt_refresh_token_required()
        subject = await self.Authorize.get_jwt_subject()
        new_access_token = self.Authorize.create_access_token(subject=subject)
        return {"access_token": new_access_token}

    async def get_current_user(
        self,
        credentials: HTTPAuthorizationCredentials,
    ) -> User:
        """Get the current user from JWT and validate the token type."""
        try:
            # Validate the token and get the raw JWT data
            await self.Authorize.jwt_required()
            subject = await async_json_loads(await self.Authorize.get_jwt_subject())
            user_id = subject['id']
            
            return await self.user_storage.get_user_by_id(user_id, session=self.session)
        except Exception as e:
            raise e
    
    async def is_denied(self, jti):
        # Check if the token is in the denied list
        if await self.cache.exists(jti):
            raise HTTPException(status_code=401, detail="Token has been denied")

    async def validate(self, actual_token_type: str, required_type: str):
        if actual_token_type != required_type:
            raise HTTPException(
                status_code=403,
                detail=f"{required_type.capitalize()} token required. Please use a {required_type} token."
            )


async def get_authentication_service(
    session: AsyncSession = Depends(get_async_session),
    user_storage: IUserStorage = Depends(get_user_storage),
    hasher: IHasher = Depends(get_data_hasher),
    cache: ICasheClient = Depends(get_redis_client),
    authorize: AuthJWT = Depends(),
) -> AuthenticationService:
    return AuthenticationService(
        user_storage,
        hasher,
        cache,
        session,
        authorize,
    )


async def get_auth_credentials(
        credentials: HTTPAuthorizationCredentials = Depends(CustomHTTPBearer()),
        authorize: AuthJWT = Depends(),
    ):
    await authorize.jwt_required()
    await authorize.get_raw_jwt()
    return credentials


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(CustomHTTPBearer()),
        service: IAuthenticationService = Depends(get_authentication_service),
        ) -> User:
    return await service.get_current_user(credentials)
