from datetime import datetime
from pathlib import Path

from app.services.holiday_service import HolidayService
from app.schemas.holiday import Holiday


class HolidayController(object):
    def __init__(self):
        self.holiday_service = HolidayService()

    async def get_for_date(self, date: datetime) -> Holiday | None:
        return await self.holiday_service.get_for_date(date)


def holiday_controller() -> Holiday | None:
    return HolidayController()
