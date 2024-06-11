from app.controllers.base import ControllerBase
from app.modules.transit import Transit


class PoiController(ControllerBase):
    async def get_payment_by_poi(self, start, end) -> int:
        transit = Transit()
        start_lng, start_lat = await transit.get_coordinate_by_station_name(
            station_name=start
        )
        end_lng, end_lat = await transit.get_coordinate_by_station_name(
            station_name=end
        )
        fare = await transit.get_payment_by_coordinate(
            sx=start_lng, sy=start_lat, ex=end_lng, ey=end_lat
        )
        return fare
