from app.controllers.base import ControllerBase
from app.modules.transit import Transit


class PoiController(ControllerBase):
    async def get_payment_by_poi(
        self,
        start: str,
        end: str,
        start_station_type: str,
        end_station_type: str,
    ) -> int:
        transit = Transit()
        start_lng, start_lat = await transit.get_coordinate_by_station_name(
            station_name=start, station_type=start_station_type
        )
        end_lng, end_lat = await transit.get_coordinate_by_station_name(
            station_name=end, station_type=end_station_type
        )
        fare = await transit.get_payment_by_coordinate(
            sx=start_lng, sy=start_lat, ex=end_lng, ey=end_lat
        )
        return fare
