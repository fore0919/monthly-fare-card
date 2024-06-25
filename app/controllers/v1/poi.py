from app.constant.location import STATION_TYPE
from app.controllers.base import ControllerBase
from app.modules.transit import Transit


class PoiController(ControllerBase):
    async def get_payment_by_poi(
        self, start: str, end: str, station_type: str
    ) -> int:
        transit = Transit()
        _type = STATION_TYPE[station_type]
        start_lng, start_lat = await transit.get_coordinate_by_station_name(
            station_name=start, station_type=_type
        )
        end_lng, end_lat = await transit.get_coordinate_by_station_name(
            station_name=end, station_type=_type
        )
        fare = await transit.get_payment_by_coordinate(
            sx=start_lng, sy=start_lat, ex=end_lng, ey=end_lat
        )
        return fare
