import csv

from sqlalchemy.ext.asyncio import AsyncSession


async def bulk_insert_station_data(
    session: AsyncSession, file_path: str
) -> None:
    with open(file=file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        stations = [Station(id=int(row["id"])) for row in reader]
        session.bulk_save_objects(stations)
    await session.commit
