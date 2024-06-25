from app.core.config import settings
from app.helper.http import Http
from app.utils.exception import DataNotFoundError, NotOKResponseError


class Transit:
    def __init__(self) -> None:
        self.api_key = settings.ODSAY_API_KEY
        self.host = "https://api.odsay.com/v1/api/"

    async def get_coordinate_by_station_name(
        self,
        station_name: str,
        station_type: str,
    ) -> tuple[float, float]:
        url = self.host + "searchStation"
        params = {
            "apiKey": self.api_key,
            "stationName": station_name,
            "stationClass": station_type,
        }
        status_code, response = await Http.get(url=url, params=params)

        if status_code == 200:
            if not response["result"]["station"]:
                raise DataNotFoundError(
                    "역 또는 정류장 정보를 찾을 수 없습니다."
                )
            lng = response["result"]["station"][0]["x"]
            lat = response["result"]["station"][0]["y"]
            return lng, lat
        else:
            raise NotOKResponseError()

    async def get_payment_by_coordinate(
        self, sx: float, sy: float, ex: float, ey: float
    ) -> int:
        url = self.host + "searchPubTransPathT"
        params = {
            "apiKey": self.api_key,
            "SX": sx,
            "SY": sy,
            "EX": ex,
            "EY": ey,
        }
        status_code, response = await Http.get(url=url, params=params)

        if status_code == 200:
            if not response["result"]["path"]:
                raise DataNotFoundError("좌표 정보를 찾을 수 없습니다.")
            payment = response["result"]["path"][0]["info"]["payment"]
            return payment
        else:
            raise NotOKResponseError()
