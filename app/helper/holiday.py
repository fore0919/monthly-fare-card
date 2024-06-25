import calendar
from datetime import date, datetime, timedelta
from typing import Any

from app.modules.holiday import Holiday


async def get_days(year: str, month: str) -> int:
    count = 0
    _, last_day = calendar.monthrange(int(year), int(month))
    first_date = date(year=int(year), month=int(month), day=1)
    last_date = date(year=int(year), month=int(month), day=last_day)
    dates = [
        (first_date + timedelta(days=i))
        for i in range((last_date - first_date).days + 1)
    ]
    h = Holiday()
    monthly_holidays = await h.get_holidays(year, month)
    holidays = await parse_holidays(monthly_holidays)
    for d in dates:
        if d.weekday() < 5:
            count += 1
        if d in holidays:
            count -= 1
    return count


async def parse_holidays(dates: list[str | None]) -> list[date | None]:
    holidays = []
    if dates:
        for d in dates:
            _date = datetime.strptime(str(d["locdate"]), "%Y%m%d")
            holidays.append(_date.date())
    return holidays
