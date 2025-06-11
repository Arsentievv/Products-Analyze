from dataclasses import dataclass
from src.tracking.repository import ProductTrackRepository
from src.tracking import schemas
from src.tracking.exceptions import ProductTrackNotFoundError
from src.users.services import UserService
from src.products.services import ProductService


@dataclass
class ProductTrackService:
    """
    Класс сервисного слоя, в котором представлена основная
    бизнес логика работы с отслеживаниями.
    """
    track_repository: ProductTrackRepository
    user_service: UserService
    product_service: ProductService

    @staticmethod
    async def _create_schema(track) -> schemas.ProductTrackSchema:
        """
        Метод для представления объекта базы в pydentic модель.
        :param track: ProductTrack
        :return: schemas.ProductTrackSchema
        """
        track = schemas.ProductTrackSchema(
            id=track.id,
            user_id=track.user_id,
            product_id=track.product_id,
            is_active=track.is_active,
            creation_date=track.creation_date
        )
        return track

    async def create_track(
            self, user_id: int, product_id: int
    ) -> schemas.ProductTrackSchema:
        """
        Сервисный метод создания отслеживания.
        :param user_id: ID пользователя.
        :param product_id: ID продукта.
        :return: schemas.ProductTrackSchema
        """

        user = await self.user_service.get_user_by_id(user_id)
        product = await self.product_service.get_product_by_id(product_id)

        if user and product:
            track = await self.track_repository.create_track(
                user_id=user_id,
                product_id=product_id
            )
            return await self._create_schema(track)

    async def get_track_by_id(self, track_id: int) -> schemas.ProductTrackSchema:
        """
        Сервисный метод получения отслеживания по ID.
        :param track_id: ID отслеживания.
        :return: schemas.ProductTrackSchema
        """

        track = await self.track_repository.get_track_by_id(track_id)
        if track:
            return await self._create_schema(track)
        else:
            raise ProductTrackNotFoundError()

    async def get_all_tracks(self) -> list[schemas.ProductTrackSchema]:
        """
        Сервисный метод получения из базы всех отслеживаний.
        :return: list[schemas.ProductTrackSchema]
        """

        tracks = await self.track_repository.get_all_tracks()
        track_schemas = [await self._create_schema(track) for track in tracks]
        return track_schemas

    async def delete_track(self, track_id: int) -> None:
        """
        Сервисный метод удаления отслеживания из базы.
        :param track_id: ID отслеживания.
        :return: None
        """
        track = await self.get_track_by_id(track_id)
        if track:
            await self.track_repository.delete_track(track_id)

