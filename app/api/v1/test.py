from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.v1 import v1_controllers as v1_con
from app.schemas.base import CreateOutput
from app.utils.deps import get_session

test_router = router = APIRouter(prefix="/test")


@router.get("/{id}", response_model=CreateOutput, name="테스트 데이터 가져오기")
async def get_test_data(
    session: AsyncSession = Depends(get_session),
    id: int = Path(description="ID"),
):
    data = await v1_con.test_con.get_by_id(session=session, id=id)
    return {"id": data.id}
