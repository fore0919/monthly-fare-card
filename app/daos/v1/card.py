from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos.mixin import ModelMixin
from app.models import Card


class CardDao(ModelMixin[Card]):
    async def get_card(self, session: AsyncSession, location_id: int) -> Card:
        if not session:
            for data in self.json_data:
                if data["location_id"] == location_id:
                    return Card.from_json(data)

        return await session.scalar(
            select(Card).where(Card.location_id == location_id)
        )

    async def get_climate_card(self, session: AsyncSession) -> Card:
        if not session:
            for data in self.json_data:
                if data["location_id"] == 4:
                    return Card.from_json(data)

        card = await session.scalar(select(Card).where(Card.location_id == 4))
        return card


card_dao = CardDao(Card)
