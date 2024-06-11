from app.daos.mixin import ModelMixin
from app.models import Card, DiscountInfo


class CardDao(ModelMixin[Card]):
    pass


class DiscountInfoDao(ModelMixin[DiscountInfo]):
    pass


card_dao = CardDao(Card)
discount_info_dao = DiscountInfoDao(DiscountInfo)
