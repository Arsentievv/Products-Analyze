from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, insert, select
from src.tracking.models import ProductTrack


@dataclass
class ProductTrackRepository:
    db: AsyncSession

    async def create_track(
            self, user_id: int, product_id: int
    ) -> ProductTrack:
        """
        Метод добавления отслеживания в базу данных.
        :param user_id: ID пользователя.
        :param product_id: ID товара.
        :return: ProductTrack
        """

        query = insert(ProductTrack).values(
            user_id=user_id,
            product_id=product_id
        ).returning(ProductTrack.id)

        track_id = await self.db.execute(query)
        await self.db.commit()

        track = await self.get_track_by_id(track_id.scalar_one_or_none())
        return track

    async def get_track_by_id(self, track_id: int) -> ProductTrack:
        """
        Метод получения отслеживания по ID.
        :param track_id: ID отслеживания.
        :return: ProductTrack
        """

        query = select(ProductTrack).where(ProductTrack.id == track_id)
        track = await self.db.execute(query)
        return track.scalar_one_or_none()

    async def get_all_tracks(self) -> list[ProductTrack]:
        """
        Метод получения из базы всех отслеживаний.
        :return: list[ProductTrack]
        """

        query = select(ProductTrack)
        tracks = await self.db.execute(query)
        return tracks.scalars().all()

    async def delete_track(self, track_id: int) -> None:
        """
        Метод удаления отслеживания из базы.
        :param track_id: ID отслеживания.
        :return: None
        """

        query = delete(ProductTrack).where(ProductTrack.id == track_id)
        await self.db.execute(query)
        await self.db.commit()
