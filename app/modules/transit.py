from app.constant.location import StationType
from app.core.config import settings
from app.helper.http import Http
from app.utils.exception import DataNotFoundError, NotOKResponseError


class Transit:
    def __init__(self) -> None:
        self.api_key = settings.TMAP_API_KEY
        self.host = "https://apis.openapi.sk.com"

    async def get_coordinate_by_station_name(
        self,
        station_name: str,
        station_type: str | None = None,
    ) -> tuple[float, float]:
        url = self.host + "/tmap/pois"
        headers = {
            "Accept": "application/json",
            "appKey": self.api_key,
        }
        params = {
            "version": 1,
            "searchKeyword": station_name,
            "count": 5,
        }
        if station_type != StationType.ALL:
            params["searchKeyword"] += f"&{station_type.value}"
        status_code, response = await Http.get(
            url=url, headers=headers, params=params
        )

        if status_code == 200:
            if not response:
                raise DataNotFoundError(
                    "역 또는 정류장 정보를 찾을 수 없습니다."
                )
            lng = response["searchPoiInfo"]["pois"]["poi"][0]["frontLon"]
            lat = response["searchPoiInfo"]["pois"]["poi"][0]["frontLat"]
            return lng, lat
        else:
            raise NotOKResponseError()

    async def get_payment_by_coordinate(
        self, sx: float, sy: float, ex: float, ey: float
    ) -> int:
        url = self.host + "/transit/routes"
        headers = {
            "Accept": "application/json",
            "appKey": self.api_key,
        }
        payload = {
            "startX": sx,
            "startY": sy,
            "endX": ex,
            "endY": ey,
        }
        status_code, response = await Http.post(
            url=url, headers=headers, json=payload
        )

        if status_code == 200:
            if not response:
                raise DataNotFoundError("좌표 정보를 찾을 수 없습니다.")
            payment = response["metaData"]["plan"]["itineraries"][0]["fare"][
                "regular"
            ]["totalFare"]
            return payment
        else:
            raise NotOKResponseError(
                url=url,
                response_status_code=status_code,
                request_data=payload,
                response_data=response["error"],
            )
