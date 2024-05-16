from typing import Iterator, Optional
from datetime import datetime, timedelta
import pendulum
from loguru import logger

from app.schemas.date_dimension import DateDimension
from app.schemas.holiday import Holiday
from app.services.holiday_service import HolidayService


class DateDimensionService(object):
    def __init__(self, holiday_service: HolidayService):
        self.holiday_service = holiday_service

    def get_for_date(self, date: datetime) -> list[DateDimension]:
        """
        根据给定的完整日期时间返回0~23小时的DateDimension对象列表
        :param date: 完整的日期时间，datetime对象
        :return: DateDimension列表
        """
        date_dimensions = []
        for hour in range(24):
            date_hour = date.replace(hour=hour)
            date_dimensions.append(self.__get_for_date_hour(date_hour))

        return date_dimensions

    def __get_for_date_hour(self, date: datetime) -> DateDimension:
        """
        根据给定的完整日期时间返回一个DateDimension对象
        :param date: 完整的日期时间，datetime对象
        :return: DateDimension对象
        """
        logger.debug(f"get_for_date_hour: {date}")

        pendulum_date = pendulum.datetime(
            date.year,
            date.month,
            date.day,
            date.hour,
            date.minute,
            date.second,
            tz="Asia/Shanghai",
        )

        prev_year = pendulum_date.subtract(years=1)
        prev_month = (
            (pendulum_date.subtract(months=1))
            if pendulum_date.month != 1
            else pendulum_date.end_of("year")
        )
        prev_day = (
            (pendulum_date.subtract(days=1))
            if pendulum_date.day != 1
            else prev_month.end_of("month")
        )

        hour = pendulum_date.hour

        # 计算班次
        shift = "夜" if hour < 8 else "早" if hour < 17 else "中"

        # 计算假日
        holiday = self.holiday_service.get_for_date(pendulum_date)

        return DateDimension(
            # 日期
            date_id=pendulum_date.format("YYYYMMDD"),
            date_hour_id=pendulum_date.format("YYYYMMDDHH"),
            date=pendulum.parse(pendulum_date.to_date_string()),
            date_time=pendulum.parse(pendulum_date.to_datetime_string()),
            # 年
            year=str(pendulum_date.year),
            year_start_date=pendulum_date.start_of("year"),
            year_end_date=pendulum_date.end_of("year"),
            # /季度
            quarter=f"Q{pendulum_date.quarter}",
            year_quarter=f"{pendulum_date.year}Q{pendulum_date.quarter}",
            # /月
            month=str(pendulum_date.month),
            month_start_date=pendulum_date.start_of("month"),
            month_end_date=pendulum_date.end_of("month"),
            # 周
            weekday=pendulum_date.format("E"),
            week_identifier=pendulum_date.format("ddd"),
            # 第几天
            day=str(pendulum_date.day),
            day_of_year=pendulum_date.day_of_year,
            day_of_month=pendulum_date.day,
            day_of_week=pendulum_date.day_of_week + 1,  # 星期一为1
            # 第几周
            week_of_month=pendulum_date.week_of_month,
            week_of_year=pendulum_date.week_of_year,  # 当年周数，星期一为第一周
            # 日类型
            is_weekend="Yes" if pendulum_date.day_of_week >= 5 else "No",
            date_type=self.__get_date_type(pendulum_date, holiday),
            holiday_name=holiday.name if holiday else "",
            # 小时/班次
            hour=str(hour),
            shift=shift,
            # 去年日期
            prev_year_date=prev_year,
            prev_year_date_id=prev_year.format("YYYYMMDD"),
            prev_year_date_time=pendulum.parse(prev_year.to_datetime_string()),
            prev_year_start_date=prev_year.start_of("year"),
            prev_year_end_date=prev_year.start_of("year"),
            prev_year=str(prev_year.year),
            prev_year_month=str(prev_month.month),
            prev_month_start_date=prev_month.start_of("month"),
            prev_month_end_date=prev_month.end_of("month"),
            prev_year_day=str(prev_year.day),
        )

    def __get_date_type(
        self, date: datetime.date, holiday: Optional[Holiday]
    ) -> str:
        """
        根据给定的日期和假期信息，判断日期的类型（工作日、休息日、节假日）。

        参数:
        date: datetime.date - 需要判断类型的日期。
        holiday: Optional[Holiday] - 假期信息对象，可选。

        返回值:
        str - 日期的类型，可能的取值为 "工作日"、"休息日"、"节假日"。
        """
        # 判断是否为工作日
        is_workday = date.weekday() < 5
        # 判断是否为节假日
        is_off_day = holiday and holiday.is_offday if holiday else False

        # 默认情况下，将日期类型设为"工作日"
        date_type = "工作日"
        # 如果不是工作日，则将日期类型设为"休息日"
        if not is_workday:
            date_type = "休息日"

        # 如果是节假日，则将日期类型设为"节假日"，否则保持为"工作日"
        if is_off_day:
            date_type = "节假日"
        else:
            date_type = "工作日"

        return date_type

    def get_ste_day(
        self, time_start: datetime, time_end: datetime
    ) -> list[DateDimension]:
        """
        根据给定的日期范围，计算并返回每个日期对应的DateDimension对象列表。

        参数:
        time_start: datetime.date - 日期范围的开始时间。
        time_end: datetime.date - 日期范围的结束时间。

        返回值:
        List[DateDimension] - 日期范围内每个日期对应的DateDimension对象列表。
        """
        date_dimensions = []
        for date in self.__iter_days(time_start, time_end):
            date_dimension = self.get_for_date(date)
            date_dimensions.extend(date_dimension)

        return date_dimensions

    def __iter_days(
        self, start_date: datetime.date, end_date: datetime.date
    ) -> Iterator[datetime.date]:
        for n in range((end_date - start_date).days + 1):
            yield start_date + timedelta(days=n)
