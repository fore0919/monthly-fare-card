from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.daos.mixin import ModelMixin
from app.models import Card, DiscountInfo


class CardDao(ModelMixin[Card]):
    async def get_card(session: AsyncSession, location_id: int) -> Card:
        card = await session.scalar(
            select(Card)
            .where(Card.location_id == location_id)
            .options(joinedload(Card.discount_info))
        )
        return card

    async def get_climate_card(session: AsyncSession) -> Card:
        card = await session.scalar(
            select(Card)
            .where(Card.location_id.is_(None))
            .options(joinedload(Card.discount_info))
        )
        return card


class DiscountInfoDao(ModelMixin[DiscountInfo]):
    pass


card_dao = CardDao(Card)
discount_info_dao = DiscountInfoDao(DiscountInfo)
