from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.base import ControllerBase
from app.helper.logger import LogHelper


class LogController(ControllerBase):
    async def write_log(
        self, session: AsyncSession, log: LogHelper, data: dict
    ) -> None:
        await self.daos.v1.log.create(
            session=session,
            data=data,
            hash_id=log.hash_id,
            remote_addr=log.client_ip,
            url=log.url,
            method=log.method,
        )
