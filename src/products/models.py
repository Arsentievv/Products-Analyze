from src.infrastructure.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)

    product_tracks: Mapped[list["ProductTrack"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"ID: {self.id} Title: {self.title}"
