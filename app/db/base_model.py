from datetime import datetime
from typing import Annotated

from sqlalchemy import String, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry


class StrType:
    str_255 = Annotated[str, 255]
    str_100 = Annotated[str, 100]
    str_64 = Annotated[str, 64]
    str_32 = Annotated[str, 32]
    str_16 = Annotated[str, 16]


class Base(AsyncAttrs, DeclarativeBase):
    __tablename__: str

    registry = registry(
        type_annotation_map={
            StrType.str_255: String(255),
            StrType.str_100: String(100),
            StrType.str_64: String(64),
            StrType.str_32: String(32),
            StrType.str_16: String(16),
        }
    )


class TimeStamps:
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(), server_default=func.now(), comment="생성시각"
    )
    updated_at: Mapped[datetime | None] = mapped_column(comment="수정시각")
    removed_at: Mapped[datetime | None] = mapped_column(comment="삭제시각")

    def remove(self) -> None:
        self.removed_at = datetime.now()
