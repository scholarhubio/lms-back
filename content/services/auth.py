from abc import ABC, abstractmethod

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials

from interfaces.storage import IUserStorage
from interfaces.hasher import IHasher

from models.users.choices import RoleType
from models.users.models import User
from storages.user import get_user_storage

from core.security import CustomHTTPBearer
from core.hasher import get_data_hasher

from schemas.auth import UserRegistration, UserLogin, ValidPhoneBase, UserVerification

from db.postgres import get_async_session
from db.redis import get_redis_client, ICasheClient

from sqlalchemy.ext.asyncio import AsyncSession
from async_fastapi_jwt_auth import AuthJWT
from datetime import datetime, timezone
from core.utils import async_json_dumps, async_json_loads
from broadcast.playmobile import get_playmobile, SMSClient
from exceptions import CodeAlreadySent, UnverifiedUser, CodeExpired
from schemas.auth import AuthSettingsSchema
import random


verification_template = "verified_phone:{phone}"


class IAuthenticationService(ABC):
    @abstractmethod
    async def register_student(self):
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

    @abstractmethod
    async def send_unique_code(self, data: ValidPhoneBase) -> int:
        pass

    async def verify_code(self, data: UserVerification):
        pass


class AuthenticationService:
    def __init__(
        self,
        user_storage: IUserStorage,
        hasher: IHasher,
        cache: ICasheClient,
        session: AsyncSession,
        Authorize: AuthJWT,
        sms_client: SMSClient,
    ):
        self.user_storage = user_storage
        self.hasher = hasher
        self.cache = cache
        self.session = session
        self.Authorize = Authorize
        self.sms_client = sms_client

    async def send_unique_code(self, data: ValidPhoneBase) -> int:
        await self.check_user(phone=data.phone)
        random_number = await self.generate_unique_code_for_user(data.phone)
        text = f"""ScholarHub Platform

        verification code: {random_number}
        """
        recipients = [await self.generate_recipient_data(data.phone, text)]
        await self.sms_client.send_message(recipients)
        await self.cache.setex(data.phone, 30, random_number)

    async def verify_code(self, data: UserVerification):
        code = await self.cache.get_from_cashe(data.phone)
        if str(code) != str(data.code) or not code:
            raise CodeExpired
        key = verification_template.format(phone=data.phone)
        await self.cache.setex(key, 3600, data.phone)

    async def check_user(self, phone: str) -> User:
        stored_user = await self.user_storage.get_user_by_phone(phone, session=self.session)
        if stored_user:
            raise HTTPException(status_code=400, detail="User already exists.")
        return stored_user

    async def register_student(self, user: UserRegistration):
        """Register a new user."""
        key = verification_template.format(phone=user.phone)
        verified_phone = await self.cache.get_from_cashe(key)
        if not verified_phone or verified_phone != user.phone:
            raise UnverifiedUser

        await self.check_user(phone=user.phone)
        hashed_password = await self.hasher.hash_password(user.password)
        await self.create_user(RoleType.STUDENT, user.phone, hashed_password)
        await self.cache.delete(key)

    async def create_user(self, role, phone: str, password):
        """Register a new user."""
        await self.user_storage.create_new_user(
            phone=phone, password=password,
            role=role, session=self.session)

    async def login_user(self, user: UserLogin):
        """Login the user and return access and refresh tokens."""
        stored_user = await self.user_storage.get_user_by_phone(user.phone, session=self.session)
        if not stored_user:
            raise HTTPException(status_code=400, detail="Invalid username or password.")
        if stored_user.role != RoleType.STUDENT.value:
            raise UnverifiedUser
        verified_pass = await self.hasher.verify_password(user.password, stored_user.password)
        if verified_pass == False or not verified_pass:
            raise HTTPException(status_code=400, detail="Invalid username or password.")

        # Create a subject dict that includes user details
        subject = await async_json_dumps({"id": str(stored_user.id), "role": stored_user.role})

        # Generate access and refresh tokens with the customized subject
        access_token = await self.Authorize.create_access_token(subject=subject, user_claims={"type": "access"}, expires_time=AuthSettingsSchema().access_expires)
        refresh_token = await self.Authorize.create_refresh_token(subject=subject, user_claims={"type": "refresh"}, expires_time=AuthSettingsSchema().refresh_expires)
        return {"access_token": str(access_token), "refresh_token": str(refresh_token)}

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

    async def generate_unique_code_for_user(self, phone: str) -> int:
        exists = await self.cache.exists(phone)
        if exists == True:
            raise CodeAlreadySent
        random_number = random.randrange(1000, 10000)
        return random_number

    async def generate_recipient_data(self, phone: str, text: str):
        return {
            "phone": phone,
            "text": text
        }


async def get_authentication_service(
    session: AsyncSession = Depends(get_async_session),
    user_storage: IUserStorage = Depends(get_user_storage),
    hasher: IHasher = Depends(get_data_hasher),
    cache: ICasheClient = Depends(get_redis_client),
    authorize: AuthJWT = Depends(),
    sms_client: SMSClient = Depends(get_playmobile),
) -> AuthenticationService:
    return AuthenticationService(
        user_storage,
        hasher,
        cache,
        session,
        authorize,
        sms_client=sms_client,
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
