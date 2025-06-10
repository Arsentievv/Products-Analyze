from dataclasses import dataclass

from src.products.exceptions import ProductNotFoundError
from src.products.repository import ProductRepository
from src.products.parser import WBDataParser
from src.products import schemas


@dataclass
class ProductService:
    product_repository: ProductRepository

    async def create_product(self, product_url) -> schemas.ProductSchema:
        """
        Сервисный метод добавления товара в базу данных.
        :param product_url: URL товара.
        :return: Product
        """
        wb_parser = WBDataParser(product_url)
        data_dict = await wb_parser.make_data_dict()
        product = await self.product_repository.create_product(
            title=data_dict.get("title"),
            price=data_dict.get("price"),
            url=product_url,
        )
        return schemas.ProductSchema(
            id=product.id,
            title=product.title,
            price=product.price,
            url=product.url
        )

    async def get_product_by_id(self, product_id: int) -> schemas.ProductSchema:
        """
        Сервисный метод получения из базы данных товара по ID.
        :param product_id: ID товара.
        :return: Product
        """
        product = await self.product_repository.get_product_by_id(product_id)
        if product:
            return schemas.ProductSchema(
                id=product.id,
                title=product.title,
                price=product.price,
                url=product.url
            )
        else:
            raise ProductNotFoundError()

    async def get_all_products(self) -> list[schemas.ProductSchema]:
        """
        Сервисный метод получения всех товаров из базы данных.
        :return: list[Product]
        """
        products = await self.product_repository.get_all_products()
        products_list = [schemas.ProductSchema(
            id=product.id, title=product.title, price=product.price, url=product.url) for product in products
        ]
        return products_list

    async def delete_product(self, product_id: int) -> None:
        """
        Сервисный метод удаления товара из базы данных.
        :param product_id: ID товара.
        :return: None
        """
        product = await self.product_repository.get_product_by_id(product_id)
        if product:
            await self.product_repository.delete_product(product_id)
        else:
            raise ProductNotFoundError()
