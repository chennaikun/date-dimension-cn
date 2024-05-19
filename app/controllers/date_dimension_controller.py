from datetime import datetime
from typing import AsyncGenerator, Generator

from app.schemas.date_dimension import DateDimension
from app.services.date_dimension_service import DateDimensionService
from app.services.holiday_service import HolidayService


class DateDimensionController(object):
    def __init__(self):
        self.holiday_service = HolidayService()
        self.date_dimension_service = DateDimensionService(
            self.holiday_service
        )

    async def get_for_date(self, date: datetime) -> list[DateDimension] | None:
        return [
            d async for d in self.date_dimension_service.get_for_date(date)
        ]

    async def get_ste_day(
        self, time_start: datetime, time_end: datetime
    ) -> list[DateDimension] | None:
        return [
            d
            async for d in self.date_dimension_service.get_ste_day(
                time_start, time_end
            )
        ]

    async def generate_csv(
        self, time_start: datetime, time_end: datetime
    ) -> AsyncGenerator[DateDimension, None]:
        # 动态获取属性名作为表头

        yield ",".join(
            field_name for field_name in DateDimension.model_fields.keys()
        ).encode("utf-8")

        yield "\n"
        # 写入数据
        async for d in self.date_dimension_service.get_ste_day(
            time_start, time_end
        ):
            yield ",".join(str(v) for v in d.model_dump().values()).encode(
                "utf-8"
            )
            yield "\n"


def date_dimension_controller():
    return DateDimensionController()
