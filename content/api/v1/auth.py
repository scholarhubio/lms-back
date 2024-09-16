from fastapi import APIRouter, Depends, Form, Header, status
from services.auth import get_authentication_service, IAuthenticationService
from schemas.auth import UserLogin, UserRegistration, ValidPhoneBase, UserVerification
from schemas.responses.auth import UserSignIn
from typing import Annotated


router = APIRouter(prefix="/auth")


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def registrate(
    user: Annotated[UserRegistration, Form()],
    service: IAuthenticationService = Depends(get_authentication_service),
    ):
    await service.register_student(user)


@router.post("/signin", status_code=status.HTTP_200_OK)
async def signin(
    user: Annotated[UserLogin, Form()],
    service: IAuthenticationService = Depends(get_authentication_service),
    agent: str = Header(...),
    ) -> UserSignIn:
    return await service.login_user(user)


@router.post("/signout", status_code=status.HTTP_200_OK)
async def signout(
    service: IAuthenticationService = Depends(get_authentication_service),
    ):
    return await service.logout_user()


@router.post("/send-code", status_code=status.HTTP_200_OK)
async def send_code(
    data: Annotated[ValidPhoneBase, Form()],
    service: IAuthenticationService = Depends(get_authentication_service),
    ):
    return await service.send_unique_code(data)


@router.post("/verify-code", status_code=status.HTTP_200_OK)
async def send_code(
    data: Annotated[UserVerification, Form()],
    service: IAuthenticationService = Depends(get_authentication_service),
    ):
    return await service.verify_code(data)
