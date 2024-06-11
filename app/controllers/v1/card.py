from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.base import ControllerBase
from app.helper.age_calc import get_age
from app.helper.holiday import get_days
from app.schemas.card import FareCardOutput, FareCardSchema

if TYPE_CHECKING:
    from app.models import Test


class CardController(ControllerBase):
    async def get_bast_card(
        self,
        session: AsyncSession,
        user_birth_date: str,
        user_area: str,
        fare: int,
        year: str,
        month: str,
    ) -> FareCardOutput:
        age = await get_age(user_birth_date)
        days = await get_days(year, month)
        monthly_fare = fare * days

        return FareCardOutput(
            total_count=days,
            total_payment=monthly_fare,
            best_card=FareCardSchema(name=,discount_rate=,discount_type=,discounted_cost=,payment=)
        )
