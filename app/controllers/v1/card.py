from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.base import ControllerBase
from app.helper.age_calc import get_age
from app.helper.holiday import get_days
from app.schemas.card import FareCardOutput, FareCardSchema

if TYPE_CHECKING:
    from app.models import Card, Location


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
            if age >= card.youth_age:
                discount_rate = card.discount_info.youth
                climate_card_discount = climate_card.discount_info.youth
            elif age <= card.senior_age:
                discount_rate = card.discount_info.senior
            else:
                discount_rate = card.discount_info.adult
        else:
            discount_rate = 0

        discounted_cost = monthly_fare * discount_rate / 100.0
        payment = monthly_fare - discounted_cost + (additional_count * fare)

        # TODO 기후동행 못쓰는 노선 추가

        return FareCardOutput(
            total_count=days,
            total_payment=monthly_fare,
            best_card=FareCardSchema(
                name=card.name,
                discount_rate=f"{discount_rate} %",
                discounted_cost=discounted_cost,
                payment=payment,
            ),
            climate_card=FareCardSchema(
                name=climate_card.name,
                discount_rate=climate_card_discount,
                discounted_cost=climate_card_discount,
                payment=climate_card.min_cost - climate_card_discount,
            ),
        )
