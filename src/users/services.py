from dataclasses import dataclass

from src.users.exceptions import UserNotFoundError, IncorrectPasswordError
from src.users.repository import UserRepository
from src.users import schemas, models
from datetime import datetime
from jose import jwt
from src.settings import get_settings

settings = get_settings()


@dataclass
class UserService:
    user_repository: UserRepository

    async def create_user(
            self, email: str, password: str, telegram: str
    ) -> schemas.UserLoginSchema:
        """
        Сервисный метод создания пользователя.
        :param email: Email пользователя.
        :param password: Пароль пользователя.
        :param telegram: Telegram ник пользователя.
        :return: UserLoginSchema
        """
        user = await self.user_repository.create_user(email, password, telegram)
        token = await self._generate_access_token(user_id=user.id)
        return schemas.UserLoginSchema(
            id=user.id,
            access_token=token
        )

    async def update_user(
            self,
            user_id: int,
            email: str = None,
            password: str = None,
            telegram: str = None
    ) -> schemas.UserSchema:
        """
        Сервисный метод изменения данных пользователя.
        :param user_id: ID пользователя
        :param email: Email
        :param password: Пароль
        :param telegram: Телеграм ник
        :return: User
        """
        user = await self.user_repository.get_user_by_id(user_id)
        if user:
            updated_user = await self.user_repository.update_user(
                user=user,
                email=email,
                password=password,
                telegram=telegram
            )
            return schemas.UserSchema(
                id=updated_user.id,
                email=updated_user.email,
                password=updated_user.password,
                telegram=updated_user.telegram,
                is_active=updated_user.is_active
            )
        else:
            raise UserNotFoundError()

    async def login(self, email: str, password: str) -> schemas.UserLoginSchema:
        """
        Метод авторизации пользователя.
        :param email: Email пользователя.
        :param password: Пароль пользователя.
        :return: schemas.UserLoginSchema
        """
        user = await self.user_repository.get_user_by_email(email)
        await self._validate_auth_user(user, password)
        token = await self._generate_access_token(user.id)
        return schemas.UserLoginSchema(
            id=user.id,
            access_token=token
        )

    async def get_user_by_id(self, user_id: int) -> schemas.UserSchema:
        """
        Сервисный метод получения пользователя по ID из базы данных.
        :param user_id: ID пользователя.
        :return: User
        """
        user = await self.user_repository.get_user_by_id(user_id)
        if user:
            return schemas.UserSchema(
                id=user.id,
                email=user.email,
                password=user.password,
                telegram=user.telegram,
                is_active=user.is_active
            )
        else:
            raise UserNotFoundError()

    async def get_user_by_email(self, email: str) -> schemas.UserSchema:
        """
        Сервисный метод получения пользователя по ID из базы данных.
        :param email: Email пользователя.
        :return: User
        """
        user = await self.user_repository.get_user_by_email(email)
        if user:
            return schemas.UserSchema(
                id=user.id,
                email=user.email,
                password=user.password,
                telegram=user.telegram,
                is_active=user.is_active
            )
        else:
            raise UserNotFoundError()

    async def delete_user(self, user_id: int) -> None:
        """
        Сервисный метод удаления пользователя.
        :param user_id: ID пользователя
        :return: None
        """
        user = await self.user_repository.get_user_by_id(user_id)
        if user:
            await self.user_repository.delete_user(user)
        else:
            raise UserNotFoundError

    @staticmethod
    async def _validate_auth_user(user: models.User, password: str):
        """
        Метод валидации пользовательских данных.
        :param user: models.User
        :param password: Пароль пользователя.
        :return: None
        """
        if not user:
            raise UserNotFoundError()
        if user.password != password:
            raise IncorrectPasswordError()

    @staticmethod
    async def _generate_access_token(user_id: int) -> str:
        """
        Метод генерации JWT токена.
        :param user_id: ID пользователя.
        :return: JWT
        """
        exp = datetime.now().timestamp() + 1800
        token = jwt.encode(
            {"user_id": user_id, "exp": exp}, settings.SECRET_KEY, algorithm=settings.ENCODE_ALGORYTHM
        )
        return token
