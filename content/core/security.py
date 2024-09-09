# custom_http_bearer.py
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import HTTP_403_FORBIDDEN

class CustomHTTPBearer(HTTPBearer):
    """Custom HTTPBearer class to require token in Swagger UI."""

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Invalid authentication scheme."
            )
        if not credentials.credentials:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Invalid token."
            )
        return credentials
