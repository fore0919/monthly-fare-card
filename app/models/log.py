from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import Base, TimeStamps


class Log(Base, TimeStamps):
    __tablename__ = "log"

    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[str] = mapped_column()
    hash_id: Mapped[str] = mapped_column()
    remote_addr: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()
    method: Mapped[str] = mapped_column()
