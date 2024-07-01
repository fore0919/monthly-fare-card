from .card import card_dao, discount_info_dao
from .location import location_dao
from .log import log_dao

__all__ = ["DAOs", "v1_daos"]


class DAOs:
    location = location_dao
    card = card_dao
    discount_info = discount_info_dao
    log = log_dao


v1_daos = DAOs()
