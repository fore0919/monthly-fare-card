from app.daos import DAOs


class ControllerBase:
    def __init__(self, daos: DAOs):
        self.daos = daos
