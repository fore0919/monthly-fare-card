from app.daos.mixin import ModelMixin
from app.models import Log


class LogDao(ModelMixin[Log]):
    pass


log_dao = LogDao(Log)
