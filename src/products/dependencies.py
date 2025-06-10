from fastapi import Depends
from src.products.services import ProductService
from src.products.repository import ProductRepository
from src.infrastructure.database.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated


async def get_product_repository(
        db: Annotated[AsyncSession, Depends(get_db)]
) -> ProductRepository:
    """
    Зависимость для получения методов репозитория товаров.
    :param db: Сессия.
    :return:
    """
    product_repository = ProductRepository(db)
    return product_repository


async def get_product_service(
        product_repository: Annotated[ProductRepository, Depends(get_product_repository)]
) -> ProductService:
    """
    Зависимость для получения методов сервисного слоя товаров.
    :param product_repository: ProductRepository
    :return: ProductService
    """
    product_service = ProductService(product_repository)
    return product_service