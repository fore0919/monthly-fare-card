from app.daos.mixin import ModelMixin
from app.models import Location


class LocationDao(ModelMixin[Location]):
    pass


location_dao = LocationDao(Location)
