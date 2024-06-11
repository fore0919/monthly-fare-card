from datetime import date
from typing import Optional

from constant.card import Location
from pydantic import BaseModel, Field


class FareCardInput(BaseModel):
    user_birth_date: str = Field(
        description="사용자 생년월일 (YYYY-MM-DD)", example="1995-09-19"
    )
    user_area: Location = Field(description="사용자 거주지역", example="서울")
    start: str = Field(description="출발지", example="신림역")
    end: str = Field(description="도착지", example="강남역")
    year: Optional[str] = Field(
        description="입력 연도",
        example="2024",
        default=date.today().year,
    )
    month: Optional[str] = Field(
        description="입력 월",
        example="7",
        default=date.today().month,
    )


class FareCardSchema(BaseModel):
    name: str = Field(description="카드명", example="K패스")
    discount_rate: int = Field(description="할인율", example="20")
    discount_type: str = Field(description="할인 타입", example="adult")
    discounted_cost: int = Field(description="할인 금액", example="15000")
    payment: int = Field(description="할인된 요금", example="65000")


class FareCardOutput(BaseModel):
    total_count: int = Field(description="총 이용 횟수", example="20")
    total_payment: int = Field(description="총 이용 금액", example="80000")
    best_card: FareCardSchema
