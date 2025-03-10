from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.base import ControllerBase
from app.helper.age_calc import get_age
from app.helper.holiday import get_days
from app.schemas.card import FareCardOutput, FareCardSchema

if TYPE_CHECKING:
    from app.models import Card, Location
else:
    from app.models.card import Card
    from app.models.location import Location


class CardController(ControllerBase):
    async def get_bast_card(
        self,
        session: AsyncSession,
        user_birth_date: str,
        user_area: str,
        fare: int,
        distance: float,
        year: str,
        month: str,
    ) -> FareCardOutput:
        location: Location = await self.daos.v1.location.get(
            session=session, name=user_area
        )
        card: Card = await self.daos.v1.card.get_card(
            session=session, location_id=location.id
        )
        climate_card: Card = await self.daos.v1.card.get_climate_card(
            session=session
        )
        age = await get_age(user_birth_date)
        days = await get_days(year, month)
        used_count = days * 2
        additional_count, climate_card_discount = 0, 0
        if card.max_count:
            if used_count > card.max_count:
                additional_count = used_count - card.max_count
                used_count = card.max_count
        monthly_fare = fare * used_count

        if used_count > card.min_count:
            if age <= card.youth_age:
                discount_rate = card.youth
                climate_card_discount = climate_card.youth
            elif age >= card.senior_age:
                discount_rate = card.senior
            else:
                discount_rate = card.adult
        else:
            discount_rate = 0

        discounted_cost = monthly_fare * discount_rate / 100.0
        payment = monthly_fare - discounted_cost + (additional_count * fare)

        return FareCardOutput(
            total_count=days,
            total_payment=monthly_fare,
            total_distance=distance,
            best_card=FareCardSchema(
                name=card.name,
                discount_rate=f"{discount_rate} %",
                discounted_cost=discounted_cost,
                payment=payment,
                fare=fare,
            ),
            climate_card=FareCardSchema(
                name=climate_card.name,
                discount_rate=None,
                discounted_cost=climate_card_discount,
                payment=climate_card.min_cost - climate_card_discount,
                fare=None,
            ),
        )

    async def write_log(self, session: AsyncSession, data: dict) -> None:
        await self.daos.v1.log.create(session=session, data=data)
