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
        location = await self.daos.v1.location.get(
            session=session, name=user_area
        )
        card = await self.daos.v1.card.get_card(
            session=session, location_id=location.id
        )
        discount_type
        return FareCardOutput(
            total_count=days,
            total_payment=monthly_fare,
            best_card=FareCardSchema(
                name=card.name,
                discount_rate=card.discount_info.discount_rate,
                discount_type=discount_type,
                discounted_cost=discounted_cost,
                payment=payment,
            ),
        )
