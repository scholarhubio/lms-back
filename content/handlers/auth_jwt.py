from fastapi import Request
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse


async def handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code, content={
            "detail": exc.message})
