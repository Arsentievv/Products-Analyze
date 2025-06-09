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
    status_code=status.HTTP_201_CREATED,
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
    status_code=status.HTTP_201_CREATED,
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except exceptions.IncorrectPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.put(
    "/{task_id}/update",
    response_model=schemas.UserSchema,
    status_code=status.HTTP_200_OK,
    description="Обновление пользователя."
)
async def update_user(
        user_id: int,
        user_service: Annotated[UserService, Depends(get_user_srvice)],
        email: str = Body(),
        password: str = Body(),
        telegram: str = Body()
):
    try:
        result = await user_service.update_user(
            user_id=user_id,
            email=email,
            password=password,
            telegram=telegram
        )
        return result
    except exceptions.UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.get(
    "/id/{user_id}",
    response_model=schemas.UserSchema,
    status_code=status.HTTP_200_OK,
    description="Получение пользователя по ID."
)
async def get_user_by_id(
        user_service: Annotated[UserService, Depends(get_user_srvice)],
        user_id: int
):
    try:
        user = await user_service.get_user_by_id(user_id)
        return user
    except exceptions.UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.get(
    "/email/{email}",
    response_model=schemas.UserSchema,
    status_code=status.HTTP_200_OK,
    description="Получение пользователя по email."
)
async def get_user_by_email(
        user_service: Annotated[UserService, Depends(get_user_srvice)],
        email: str
):
    try:
        user = await user_service.get_user_by_email(email)
        return user
    except exceptions.UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.delete(
    "/delete/{user_id}",
    status_code=status.HTTP_200_OK,
    description="Удалить пользователя"
)
async def delete_user(
        user_id: int,
        user_service: Annotated[UserService, Depends(get_user_srvice)]
):
    try:
        await user_service.delete_user(user_id)
        return {
            "status": f"ID: {user_id} deleted"
        }
    except exceptions.UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )