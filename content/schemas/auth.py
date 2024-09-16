from datetime import timedelta
from uuid import UUID
from core import settings
from pydantic import BaseModel, Field, field_validator
from phonenumbers import parse, is_valid_number, NumberParseException
from exceptions import InvalidPhoneNumber


class ValidPhoneBase(BaseModel):
    phone: str = Field(description="phonenumber")
    @field_validator('phone')
    def validate_phone(cls, value: str) -> str:
        try:
            phone_number = parse(value)
            if not is_valid_number(phone_number):
                raise InvalidPhoneNumber
            return value
        except NumberParseException:
            raise InvalidPhoneNumber


class UserLogin(ValidPhoneBase):
    phone: str = Field(description="phone", default='+998901231212')
    password: str


class AuthSettingsSchema(BaseModel):
    authjwt_secret_key: str = settings.auth.secret_key
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}
    authjwt_algorithm: str = settings.auth.algorithm
    authjwt_private_key: str = settings.auth.private_key
    access_expires: int = timedelta(minutes=60)
    refresh_expires: int = timedelta(days=30)


class LoginResponseSchema(BaseModel):
    access_token: str = Field(description='Access token value')
    refresh_token: str | None = Field(None, description='Refresh token value')


class JWTUserData(BaseModel):
    id: UUID
    role: str | None


class UserRegistration(ValidPhoneBase):
    phone: str = Field(description="phone", default='+998901231212')
    password: str = Field(description="password")


class UserVerification(ValidPhoneBase):
    code: int
