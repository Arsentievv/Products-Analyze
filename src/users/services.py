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
