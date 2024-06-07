from app.daos import DAOs, daos

from .test import TestController

__all__ = ["Controllers", "v1_controllers"]


class Controllers:
    def __init__(self, daos: DAOs):
        self.test_con = TestController(daos)


v1_controllers = Controllers(daos)
