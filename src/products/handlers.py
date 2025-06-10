from fastapi import APIRouter, Body, Depends, HTTPException, status
from src.products import schemas
from src.products.exceptions import ProductNotFoundError
from src.products.services import ProductService
from typing import Annotated
from src.products.dependencies import get_product_service


router = APIRouter(prefix="/products", tags=["products"])


@router.post(
    "/create",
    response_model=schemas.ProductSchema,
    status_code=status.HTTP_201_CREATED,
    description="Добавление товара в базу данных."
)
async def create_product(
        product_service: Annotated[ProductService, Depends(get_product_service)],
        url: str = Body()
):
    product = await product_service.create_product(url)
    return product


@router.get(
    "/ID/{product_id}",
    response_model=schemas.ProductSchema,
    status_code=status.HTTP_200_OK,
    description="Получения продукта по ID."
)
async def get_product_by_id(
        product_id: int,
        product_srvice: Annotated[ProductService, Depends(get_product_service)]
):
    try:
        product = await product_srvice.get_product_by_id(product_id)
        return product
    except ProductNotFoundError as e:
        raise HTTPException(
            detail=e.detail,
            status_code=status.HTTP_404_NOT_FOUND
        )


@router.get(
    "/all",
    response_model=list[schemas.ProductSchema],
    status_code=status.HTTP_200_OK,
    description="Получение всех продуктов."
)
async def get_all_products(
        product_service: Annotated[ProductService, Depends(get_product_service)]
):
    products = await product_service.get_all_products()
    return products

@router.delete(
    "/{product_id}/delete",
    status_code=status.HTTP_200_OK,
    description="Удаление товара из базы данных."
)
async def delete_product(
        product_id: int,
        product_service: Annotated[ProductService, Depends(get_product_service)]
):
    try:
        await product_service.delete_product(product_id)
        return {
            "status": f"{product_id} deleted"
        }
    except ProductNotFoundError as e:
        raise HTTPException(
            detail=e.detail,
            status_code=status.HTTP_404_NOT_FOUND
        )