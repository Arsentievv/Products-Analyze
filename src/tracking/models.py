from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infrastructure.database.base import Base
from datetime import datetime


class ProductTrack(Base):
    __tablename__ = "product_tracks"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    is_active: Mapped[bool] = mapped_column(default=True)
    creation_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="product_tracks")
    product: Mapped["Product"] = relationship(back_populates="product_tracks")

    def __repr__(self):
        return f"{self.user} {self.product}"

