from typing import TYPE_CHECKING, Any, Optional

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
    adult: Mapped[int] = mapped_column()
    youth: Mapped[int] = mapped_column()
    low: Mapped[int] = mapped_column()
    senior: Mapped[int] = mapped_column()
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    location: Mapped["Location"] = relationship(foreign_keys=[location_id])

    def __init__(
        self,
        id: int,
        name: str,
        max_count: Optional[int],
        min_count: int,
        youth_age: int,
        senior_age: int,
        min_cost: int,
        adult: int,
        youth: int,
        low: int,
        senior: Optional[int],
        location_id: Optional[int],
    ):
        self.id = id
        self.name = name
        self.max_count = max_count
        self.min_count = min_count
        self.youth_age = youth_age
        self.senior_age = senior_age
        self.min_cost = min_cost
        self.adult = adult
        self.youth = youth
        self.low = low
        self.senior = senior
        self.location_id = location_id

    def __repr__(self):
        return (
            f"Card(id={self.id}, name={self.name}, max_count={self.max_count}, "
            f"min_count={self.min_count}, youth_age={self.youth_age}, "
            f"senior_age={self.senior_age}, min_cost={self.min_cost}, "
            f"adult={self.adult}, youth={self.youth}, low={self.low}, senior={self.senior}"
            f"location_id={self.location_id})"
        )

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Card":
        return cls(
            id=data["id"],
            name=data["name"],
            max_count=data.get("max_count"),
            min_count=data["min_count"],
            youth_age=data["youth_age"],
            senior_age=data["senior_age"],
            min_cost=data["min_cost"],
            adult=data["adult"],
            youth=data["youth"],
            low=data["low"],
            senior=data["senior"],
            location_id=data.get("location_id"),
        )
