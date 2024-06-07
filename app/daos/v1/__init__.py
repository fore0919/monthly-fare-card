from .test import test_dao

__all__ = ["DAOs", "v1_daos"]


class DAOs:
    test = test_dao


v1_daos = DAOs()
