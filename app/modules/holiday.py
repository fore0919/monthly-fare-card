from app.core.config import settings
from app.helper.http import Http
from app.utils.exception import NotOKResponseError


class Holiday:
    def __init__(self) -> None:
        self.api_key = settings.HOLIDAY_API_KEY
        self.host = "http://apis.data.go.kr/B090041/openapi/service/"

    async def get_holidays(self, year: str, month: str) -> list[dict]:
        url = self.host + "SpcdeInfoService/getRestDeInfo"
        params = {
            "solYear": year,
            "solMonth": month,
            "ServiceKey": self.api_key,
            "_type": "json",
        }
        status_code, response = await Http.get(url=url, params=params)

        if status_code == 200:
            holidays = []
            if response["response"]["body"]["totalCount"] == 1:
                holidays.append(response["response"]["body"]["items"]["item"])
            elif response["response"]["body"]["totalCount"] >= 2:
                holidays.extend(response["response"]["body"]["items"]["item"])
            return holidays
        else:
            raise NotOKResponseError()
