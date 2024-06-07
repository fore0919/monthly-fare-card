from .v1 import v1_daos


class DAOs:
    def __init__(self) -> None:
        self.v1 = v1_daos


daos = DAOs()
