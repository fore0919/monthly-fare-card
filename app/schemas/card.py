from datetime import date
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field, field_validator

from app.constant.location import Location


class FareCardInput(BaseModel):
    user_birth_date: str = Query(
        description="사용자 생년월일 (YYYYMMDD)", example="19950919"
    )
    user_area: Location = Query(description="사용자 거주지역", example="서울")
    start: str = Query(description="출발지", example="신림역")
    end: str = Query(description="도착지", example="강남역")
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


class FareCardSchema(BaseModel):
    name: str = Field(description="카드명", example="K패스")
    discount_rate: str | None = Field(description="할인율", example="20")
    discounted_cost: int = Field(description="할인 금액", example="15000")
    payment: int = Field(description="할인된 요금", example="65000")


class FareCardOutput(BaseModel):
    total_count: int = Field(description="총 이용 횟수", example="20")
    total_payment: int = Field(description="총 이용 금액", example="80000")
    best_card: FareCardSchema
    climate_card: FareCardSchema
