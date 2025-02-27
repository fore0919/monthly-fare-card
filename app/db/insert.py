import csv

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.station import Line, Station


async def bulk_insert_station_data(
    session: AsyncSession, file_path: str
) -> None:
    with open(file=file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        stations = [Station(station_name=str(row["name"])) for row in reader]
        session.bulk_save_objects(stations)
    await session.commit


async def bulk_insert_line_data(session: AsyncSession, file_path: str) -> None:
    with open(file=file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        stations = [Line(line_name=str(row["lines"])) for row in reader]
        session.bulk_save_objects(stations)
    await session.commit
