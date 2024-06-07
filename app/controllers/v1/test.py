from typing import TYPE_CHECKING, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.base import ControllerBase

if TYPE_CHECKING:
    from app.models import Test


class TestController(ControllerBase):
    async def get_by_id(
        self, session: AsyncSession, id: int
    ) -> Optional["Test"]:
        user = await self.daos.v1.test.get(session=session, id=id)
        return user
