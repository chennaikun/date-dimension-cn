from datetime import datetime

from app.schemas.date_dimension import DateDimension
from app.services.date_dimension_service import DateDimensionService
from app.services.holiday_service import HolidayService


class DateDimensionController(object):
    def __init__(self):
        self.holiday_service = HolidayService()
        self.date_dimension_service = DateDimensionService(
            self.holiday_service
        )

    def get_for_date(self, date: datetime) -> DateDimension:
        return self.date_dimension_service.get_for_date(date)

    def get_ste_day(
        self, time_start: datetime, time_end: datetime
    ) -> list[DateDimension]:
        return self.date_dimension_service.get_ste_day(time_start, time_end)


def date_dimension_controller():
    return DateDimensionController()
