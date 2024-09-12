from fastapi import HTTPException, status

NotEnoughPermission = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not enough permissions")

InvalidPhoneNumber = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid phone number format")

Unauthorized = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Bad username or password")
UserCreated = HTTPException(
    status_code=status.HTTP_201_CREATED,
    detail="User has been created")
IncorrectCredentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="incorrect login or password")

RoleNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Role not found")

ServerError = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Sorry...")

ForbiddenError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You have been denied access")

UserUpdated = HTTPException(
    status_code=status.HTTP_200_OK,
    detail="User has been updated")

IntegrityError = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="record already exists")

NotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not found")


TokenDenied = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has been revoked or denied",
    headers={"WWW-Authenticate": "Bearer"},
)


AlreadyChoosen = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The answer was already choosen",
)


TaskAnswered = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The task was already answered",
)
