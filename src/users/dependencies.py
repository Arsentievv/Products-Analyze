from src.users.repository import UserRepository
from src.users.services import UserService
from src.infrastructure.database.connection import get_db
from typing import Annotated

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_repository(
        db: Annotated[AsyncSession, Depends(get_db)]
) -> UserRepository:
    """
    Зависимость для получения репозитория пользователя.
    :param db: Сессия
    :return: UserRepository
    """
    user_repository = UserRepository(db)
    return user_repository


async def get_user_srvice(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserService:
    """
    Зависимость для получения сервисного слоя пользователя.
    :param user_repository: Репозиторий пользователя.
    :return: UserService
    """
    user_service = UserService(user_repository)
    return user_service
