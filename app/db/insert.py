import csv
from collections import defaultdict

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.station import Line, Station, StationLine


async def bulk_insert_station_data(
    session: AsyncSession, file_path: str
) -> None:
    with open(file=file_path, mode="r", encoding="utf-8") as file:
        reader = list(csv.DictReader(file))

    station_dict = {}
    for row in reader:
        name = row["name"]
        if name not in station_dict:
            station_dict[name] = Station(station_name=name)
    stations = list(station_dict.values())
    session.add_all(stations)
    await session.commit()

    line_dict = {}
    for row in reader:
        line_val = row["lines"] + "호선"
        if line_val not in line_dict:
            line_dict[line_val] = Line(
                line_name=line_val, operator="서울교통공사"
            )
    lines = list(line_dict.values())
    session.add_all(lines)
    await session.commit()

    station_name_to_id = {
        station.station_name: station.id for station in stations
    }
    line_mapping = {line.line_name: line.id for line in line_dict.values()}

    groups = defaultdict(list)
    for row in reader:
        groups[row["lines"]].append(row)

    station_line_objects = []
    for line_val, group in groups.items():
        group_sorted = sorted(group, key=lambda r: int(r["id"]))
        for seq, row in enumerate(group_sorted, start=1):
            distance_val = (
                float(row["distance"])
                if row["distance"] not in ("", "NULL")
                else None
            )
            station_id = station_name_to_id.get(row["name"])
            line_id = line_mapping.get(row["lines"] + "호선")
            station_line_objects.append(
                StationLine(
                    station_id=station_id,
                    line_id=line_id,
                    sequence=seq,
                    distance_from_prev=distance_val,
                )
            )

    session.add_all(station_line_objects)
    await session.commit()
