from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.connection import get_db
from src.tracking.repository import ProductTrackRepository
from src.tracking.services import ProductTrackService
from src.users.services import UserService
from src.products.services import ProductService
from src.users.dependencies import get_user_srvice
from src.products.dependencies import get_product_service


async def get_track_repository(
        db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Зависимость для получения класса ProductTrack слоя работы с базой данных
    :param db: Сессия
    :return: ProductTrackRepository
    """
    track_repository = ProductTrackRepository(db)
    return track_repository


async def get_track_service(
        track_repository: Annotated[ProductTrackRepository, Depends(get_track_repository)],
        user_service: Annotated[UserService, Depends(get_user_srvice)],
        product_service: Annotated[ProductService, Depends(get_product_service)]
) -> ProductTrackService:
    """
    Зависимость для получения класса ProductTrack сервисного слоя.
    :param track_repository: ProductTrackRepository
    :param user_service: UserService
    :param product_service:ProductService
    :return:ProductTrackService
    """
    track_service = ProductTrackService(
        track_repository,
        user_service,
        product_service
    )
    return track_service