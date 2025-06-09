from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from src.users.models import User
from dataclasses import dataclass


@dataclass
class UserRepository:
    db: AsyncSession

    async def create_user(self, email, password, telegram) -> User:
        """
        Метод добавления пользователя в базу данных.
        :param email: Email
        :param password: Пароль
        :param telegram: Ник в телеграм
        :return: User
        """
        query = insert(User).values(
            email=email,
            password=password,
            telegram=telegram
        ).returning(User.id)
        user_id = await self.db.execute(query)
        await self.db.commit()
        return await self.get_user_by_id(user_id.scalar_one_or_none())

    async def get_user_by_id(self, user_id) -> User:
        """
        Метод получения пользователя по ID из базы данных.
        :param user_id: ID пользователя.
        :return: User
        """
        query = select(User).where(User.id == user_id)
        user = await self.db.execute(query)
        return user.scalar_one_or_none()

    async def get_user_by_email(self, user_email) -> User:
        """
        Метод получения пользователя по email из базы данных.
        :param user_email: Email пользователя.
        :return: User
        """
        query = select(User).where(User.email == user_email)
        user = await self.db.execute(query)
        return user.scalar_one_or_none()




