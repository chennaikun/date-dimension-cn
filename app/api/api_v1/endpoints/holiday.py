from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.holiday import Holiday
from app.controllers.holiday_controller import (
    HolidayController,
    holiday_controller,
)

holiday_router = APIRouter()


@holiday_router.post("/")
async def get_for_date(
    date: date,
    controller: HolidayController = Depends(holiday_controller),
) -> Holiday:
    holiday = controller.get_for_date(
        datetime.combine(date, datetime.min.time())
    )

    if holiday is None:
        raise HTTPException(status_code=404, detail="Holiday not found")

    return controller.get_for_date(date)
