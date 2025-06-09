from fastapi import APIRouter, Body, Depends, HTTPException, status
from src.users import schemas
from typing import Annotated

from src.users.dependencies import get_user_srvice
from src.users.services import UserService

from src.users import exceptions

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/create",
    response_model=schemas.UserLoginSchema,
    status_code=201,
    description="Регистрация пользователя."
)
async def create_user(
        user: schemas.UserCreateSchema,
        user_service: Annotated[UserService, Depends(get_user_srvice)]
):
    user = await user_service.create_user(user.email, user.password, user.telegram)
    return user


@router.post(
    "/login",
    status_code=201,
    response_model=schemas.UserLoginSchema,
    description="Авторизация пользователя."
)
async def login(
        user_service: Annotated[UserService, Depends(get_user_srvice)],
        email: str = Body(),
        password: str = Body()
):
    try:
        user = await user_service.login(email=email, password=password)
        return user
    except exceptions.UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )
    except exceptions.IncorrectPasswordError as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )




