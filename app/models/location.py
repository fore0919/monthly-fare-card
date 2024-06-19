from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import Base


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"{self.__tablename__}[{self.id}]"
