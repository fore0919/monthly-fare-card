from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_model import Base, TimeStamps

if TYPE_CHECKING:
    from app.models import Location


class Card(Base, TimeStamps):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    max_count: Mapped[int] = mapped_column()
    min_count: Mapped[int] = mapped_column()
    youth_age: Mapped[int] = mapped_column()
    senior_age: Mapped[int] = mapped_column()
    min_cost: Mapped[int] = mapped_column(nullable=False, default=0)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    location: Mapped["Location"] = relationship(foreign_keys=[location_id])
    discount_info: Mapped["DiscountInfo"] = relationship(
        "DiscountInfo",
        back_populates="card",
    )

    def __repr__(self):
        return f"{self.__tablename__}[{self.id}]"


class DiscountInfo(Base, TimeStamps):
    __tablename__ = "discount_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    adult: Mapped[int] = mapped_column()
    youth: Mapped[int] = mapped_column()
    low: Mapped[int] = mapped_column()
    senior: Mapped[int] = mapped_column()
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))
    card: Mapped["Card"] = relationship(
        foreign_keys=[card_id],
        back_populates="discount_info",
    )

    def __repr__(self):
        return f"{self.__tablename__}[{self.id}]"
