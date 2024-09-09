from fastapi import APIRouter, Depends, Form, Body, Header
from services.auth import get_authentication_service, IAuthenticationService, get_auth_credentials
from schemas.auth import UserLogin, UserRegistration
from typing import Annotated


router = APIRouter(prefix="/auth")


@router.post("/signup")
async def registrate(
    user: Annotated[UserRegistration, Form()],
    service: IAuthenticationService = Depends(get_authentication_service),
    ):
    return await service.register_user(user)


@router.post("/signin")
async def signin(
    user: Annotated[UserLogin, Form()],
    service: IAuthenticationService = Depends(get_authentication_service),
    agent: str = Header(...),
    ):
    return await service.login_user(user)


@router.post("/signout")
async def signout(
    service: IAuthenticationService = Depends(get_authentication_service),
    ):
    return await service.logout_user()
