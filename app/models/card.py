from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import Base


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    removed_at: Mapped[datetime | None]

    def __repr__(self):
        return f"{self.__tablename__}[{self.id}]"


class DiscountInfo(Base):
    __tablename__ = "discount_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    removed_at: Mapped[datetime | None]

    def __repr__(self):
        return f"{self.__tablename__}[{self.id}]"
