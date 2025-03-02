from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.v1 import v1_controllers as v1_con
from app.core.docs import fare_card
from app.helper.logger import LogHelper
from app.modules.request import log_request
from app.schemas.card import FareCardInput, FareCardOutput
from app.utils.deps import get_session

card_router = router = APIRouter(prefix="/best-card")


@router.get(
    path="/",
    status_code=200,
    response_model=FareCardOutput,
    name="한달 출퇴근 교통비 계산하기",
    description=fare_card,
)
async def get_best_card(
    session: AsyncSession = Depends(get_session),
    input_data: FareCardInput = Depends(FareCardInput),
    log: LogHelper = Depends(log_request),
) -> FareCardOutput:
    fare = await v1_con.poi_con.get_payment_by_poi(
        start=input_data.start,
        end=input_data.end,
        start_station_type=input_data.start_station_type,
        end_station_type=input_data.end_station_type,
    )
    result = await v1_con.card_con.get_bast_card(
        session=session,
        user_birth_date=input_data.user_birth_date,
        user_area=input_data.user_area,
        fare=fare,
        year=input_data.year,
        month=input_data.month,
    )
    if session:
        await v1_con.log_con.write_log(
            session=session, log=log, data=input_data.json()
        )
        await session.commit()
    return result
