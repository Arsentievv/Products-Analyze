from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, insert, select
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
        if user:
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

    async def update_user(
            self,
            user: User,
            email: str = None,
            password: str = None,
            telegram: str = None
    ) -> User:
        """
        Метод изменения данных пользователя.
        :param user: User
        :param email: Email
        :param password: Пароль
        :param telegram: Телеграм ник
        :return: User
        """
        if email:
            user.email = email
        if password:
            user.password = password
        if telegram:
            user.telegram = telegram
        await self.db.commit()
        return user

    async def delete_user(self, user):
        """
        Метод удаления пользователя.
        :param user: User
        :return:
        """
        query = delete(User).where(User.id == user.id)
        await self.db.execute(query)
        await self.db.commit()



