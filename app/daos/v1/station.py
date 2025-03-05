from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.daos.mixin import ModelMixin
from app.models.station import Station, StationLine


class StationDao(ModelMixin[Station]):
    async def get_station_lines(
        self, session: AsyncSession
    ) -> list[StationLine]:
        return (
            await session.scalars(
                select(StationLine).options(joinedload(StationLine.station))
            )
        ).all()

    async def get_station_lines_dict(
        self, session: AsyncSession
    ) -> list[dict[str, Any]]:
        stmt = select(StationLine, Station.station_name).join(
            Station, Station.id == StationLine.station_id
        )
        result = await session.execute(stmt)
        # result2 = (
        #     (
        #         await session.execute(
        #             select(StationLine).join(
        #                 Station, Station.id == StationLine.station_id
        #             )
        #         )
        #     )
        #     .scalars()
        #     .all()
        # )
        station_lines = []
        for sl, station_name in result.all():
            station_lines.append(
                {
                    "station_id": sl.station_id,
                    "line_id": sl.line_id,
                    "sequence": sl.sequence,
                    "distance_from_prev": (
                        float(sl.distance_from_prev)
                        if sl.distance_from_prev is not None
                        else None
                    ),
                    "name": station_name,
                }
            )
        return station_lines


station_dao = StationDao(Station)
