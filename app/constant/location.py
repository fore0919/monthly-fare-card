from enum import StrEnum


class Location(StrEnum):
    ALL = "전체"
    INCHEON = "인천"
    GYEONGGI = "경기"


class StationType(StrEnum):
    BUS = "버스"
    SUBWAY = "지하철"
    ALL = "전체"


STATION_TYPE = {"버스": "1", "지하철": "2", "ALL": "1:2"}
