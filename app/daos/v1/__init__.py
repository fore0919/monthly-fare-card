from .card import card_dao
from .location import location_dao
from .log import log_dao
from .station import station_dao

__all__ = ["DAOs", "v1_daos"]


class DAOs:
    location = location_dao
    card = card_dao
    log = log_dao
    station = station_dao


v1_daos = DAOs()
