from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import Base, TimeStamps


class Card(Base, TimeStamps):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)

    def __repr__(self):
        return f"{self.__tablename__}[{self.id}]"


class DiscountInfo(Base, TimeStamps):
    __tablename__ = "discount_info"

    id: Mapped[int] = mapped_column(primary_key=True)

    def __repr__(self):
        return f"{self.__tablename__}[{self.id}]"
