from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, insert, select
from src.products.models import Product


@dataclass
class ProductRepository:
    db: AsyncSession

    async def create_product(self, title: str, price: float, url: str) -> Product:
        """
        Метод добавления товара в базу данных.
        :param title: Наименование товара.
        :param price: Цена товара.
        :param url: URL товара.
        :return: Product
        """
        query = insert(Product).values(
            title=title,
            price=price,
            url=url
        ).returning(Product.id)
        product_id = await self.db.execute(query)
        await self.db.commit()
        return await self.get_product_by_id(product_id.scalar_one_or_none())

    async def get_product_by_id(self, product_id: int) -> Product:
        """
        Метод получения из базы данных товара по ID.
        :param product_id: ID товара.
        :return: Product
        """
        query = select(Product).where(Product.id == product_id)
        product = await self.db.execute(query)
        return product.scalar_one_or_none()

    async def get_all_products(self) -> list[Product]:
        """
        Метод получения всех товаров из базы данных.
        :return: list[Product]
        """
        query = select(Product)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def delete_product(self, product_id: int) -> None:
        """
        Метод удаления товара из базы данных.
        :param product_id: ID товара.
        :return: None
        """
        query = delete(Product).where(Product.id == product_id)
        await self.db.execute(query)
        await self.db.commit()
