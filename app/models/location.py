from typing import Any

from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import Base


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"Location(id={self.id}, name={self.name})"

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Location":
        return cls(id=data["id"], name=data["name"])
