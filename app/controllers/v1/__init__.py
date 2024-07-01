from app.daos import DAOs, daos

from .card import CardController
from .log import LogController
from .poi import PoiController

__all__ = ["Controllers", "v1_controllers"]


class Controllers:
    def __init__(self, daos: DAOs):
        self.card_con = CardController(daos)
        self.poi_con = PoiController(daos)
        self.log_con = LogController(daos)


v1_controllers = Controllers(daos)
