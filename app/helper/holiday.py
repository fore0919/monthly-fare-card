import calendar

from app.modules.holiday import Holiday


async def get_days(year: str, month: str) -> int:
    count = 0
    first_day, last_day = calendar.monthrange(year, month)[1]
    dates = [
        (first_day + last_day(days=i)).strftime("%Y-%m-%d")
        for i in range((last_day - first_day).days + 1)
    ]
    h = Holiday()
    monthly_holidays = await h.get_holidays(month)
    for date in dates:
        if date.weekday() >= 5:
            count += 1
        if date in monthly_holidays:
            count -= 1
    return count
