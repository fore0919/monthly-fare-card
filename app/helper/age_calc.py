from datetime import datetime


async def get_age(birth_day: str) -> int:
    birth = datetime.strptime(birth_day, "%Y%m%d").date()
    today = datetime.today()
    year = today.year - birth.year
    if today.month < birth.year:
        year -= 1
    elif today.month == birth.month and today.day < birth.day:
        year -= 1
    return year
