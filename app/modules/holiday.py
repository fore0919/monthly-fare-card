from datetime import date

from app.core.config import settings
from app.helper.http import Http
from app.utils.exception import NotOKResponseError


class Holiday:
    async def __init__(self) -> None:
        self.api_key = settings.HOLIDAY_API_KEY
        self.host = "http://apis.data.go.kr/B090041/openapi/service/"

    async def get_holidays(self, month: str) -> tuple[float, float]:
        url = self.host + "SpcdeInfoService"
        params = {
            "solYear": date.today().year,
            "ServiceKey": self.api_key,
            "month": month,
            "_type": "json",
        }
        response = await Http.get(url=url, params=params)

        # if response["resultCode"] == 00:
        if response.status_code == 200:
            holidays = response["Item"]["locdate"]
            return holidays
        else:
            raise NotOKResponseError()
