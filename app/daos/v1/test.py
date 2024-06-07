from app.daos.mixin import ModelMixin
from app.models import Test


class TestDao(ModelMixin[Test]):
    pass


test_dao = TestDao(Test)
