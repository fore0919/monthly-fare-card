from app.core.config import settings
from app.helper.http import Http
from app.utils.exception import NotOKResponseError


class Transit:
    async def __init__(self) -> None:
        self.api_key = settings.ODSAY_API_KEY
        self.host = "https://api.odsay.com/v1/api/"

    async def get_coordinate_by_station_name(
        self, station_name: str
    ) -> tuple[float, float]:
        url = self.host + "searchStation"
        params = {"apiKey": self.api_key, "staionName": station_name}
        response = await Http.get(url=url, params=params)

        if response.status_code == 200:
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
        response = await Http.get(url=url, params=params)

        # 요청에 성공하면, 응답에서 토큰 추출
        if response.status_code == 200:
            payment = response["result"]["path"][0]["info"]["payment"]
            return payment
        else:
            raise NotOKResponseError()
