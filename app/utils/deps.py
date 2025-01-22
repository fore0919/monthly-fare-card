from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as db:
        try:
            await db.execute(text("SELECT 1"))
        except Exception as e:
            print("Session failed to connect:", e)
            db = None
        yield db
