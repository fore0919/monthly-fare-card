from datetime import date
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field, field_validator

from app.constant.location import Location, StationType


class FareCardInput(BaseModel):
    user_birth_date: str = Query(
        description="사용자 생년월일 (YYYYMMDD)",
        default="19900101",
        example="19900101",
    )
    user_area: Location = Query(description="사용자 거주지역", example="서울")
    year: Optional[str] = Query(
        description="입력 연도",
        example="2024",
        default=date.today().year,
    )
    month: Optional[str] = Query(
        description="입력 월",
        example="7",
        default=date.today().month,
    )

    @field_validator("month")
    def month_parser(cls, v: str) -> str:
        if not v.startswith("0"):
            return "0" + v


class FareCardV1InputSchema(FareCardInput):
    start_station_type: StationType = Query(
        description="출발지 종류", example="지하철", default="지하철"
    )
    end_station_type: StationType = Query(
        description="도착지 종류", example="버스", default="지하철"
    )
    start: str = Query(description="출발지", default="합정역", example="합정역")
    end: str = Query(description="도착지", default="강남역", example="강남역")


class FareCardV2InputSchema(FareCardInput):
    start: str = Query(description="출발지", default="합정", example="합정")
    end: str = Query(description="도착지", default="강남", example="강남")

    @field_validator("start", "end")
    def station_name_parser(cls, v: str) -> str:
        if v.endswith("역") and v not in ["서울역", "신내역"]:
            return v[:-1]
        return v


class FareCardSchema(BaseModel):
    name: str = Field(description="카드명", example="K패스")
    discount_rate: str | None = Field(description="할인율", example="20")
    discounted_cost: int = Field(description="할인 금액", example=15000)
    payment: int = Field(description="할인된 요금", example=65000)
    fare: int | None = Field(description="1회 이용요금", example=1600)


class FareCardOutput(BaseModel):
    total_count: int = Field(description="총 이용 횟수", example=20)
    total_payment: int = Field(description="총 이용 금액", example=80000)
    total_distance: float = Field(description="총 이동 거리", example=20.0)
    best_card: FareCardSchema
    climate_card: FareCardSchema
