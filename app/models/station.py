from sqlalchemy import DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_model import Base


class Station(Base):
    __tablename__ = "stations"

    id: Mapped[int] = mapped_column(primary_key=True)
    station_name: Mapped[str] = mapped_column(nullable=False)
    is_departure_allowed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    is_arrival_allowed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    station_lines: Mapped[list["StationLine"]] = relationship(
        "StationLine", back_populates="station"
    )


class Line(Base):
    __tablename__ = "lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    line_name: Mapped[str] = mapped_column(nullable=False)
    operator: Mapped[str] = mapped_column(nullable=False)
    station_lines: Mapped[list["StationLine"]] = relationship(
        "StationLine", back_populates="line"
    )


class StationLine(Base):
    __tablename__ = "station_line"

    id: Mapped[int] = mapped_column("station_line_id", primary_key=True)
    station_id: Mapped[int] = mapped_column(
        ForeignKey("station.station_id"), nullable=False
    )
    line_id: Mapped[int] = mapped_column(
        ForeignKey("line.line_id"), nullable=False
    )
    sequence: Mapped[int] = mapped_column(nullable=False)
    distance_from_prev: Mapped[float] = mapped_column(
        DECIMAL(5, 2), nullable=True
    )
    station: Mapped["Station"] = relationship(back_populates="station_lines")
    line: Mapped["Line"] = relationship(back_populates="station_lines")
