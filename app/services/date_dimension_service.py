from typing import Iterator, Optional
from datetime import datetime, timedelta

from app.schemas.date_dimension import DateDimension
from app.schemas.holiday import Holiday


class DateDimensionService(object):
    def __init__(self, holiday_service):
        self.holiday_service = holiday_service

    def get_for_date(self, date: datetime) -> DateDimension:
        """
        根据给定的完整日期时间返回一个DateDimension对象
        :param date: 完整的日期时间，datetime对象
        :return: DateDimension对象
        """
        prev_year = date.year - 1
        prev_month = date.month - 1 if date.month != 1 else 12
        prev_day = (
            date.day - 1 if date.day != 1 else date.replace(prev_month).day
        )
        hour = date.hour

        # 计算班次
        shift = "夜" if hour < 8 else "早" if hour < 17 else "中"
        # 计算假日
        holiday = self.holiday_service.get_for_date(date)

        return DateDimension(
            date=date,
            date_id=date.strftime("%Y%m%d%H"),
            date_time=date,
            prev_year_same_date=date.replace(year=prev_year),
            prev_year_date_id=(date.replace(year=prev_year)).strftime(
                "%Y%m%d%H"
            ),
            prev_year_date_time=date.replace(year=prev_year),
            year=str(date.year),
            year_start_date=date.replace(month=1, day=1),
            prev_year=str(prev_year),
            prev_year_start_date=date.replace(year=prev_year, month=1, day=1),
            month=str(date.month),
            month_start_date=date.replace(day=1),
            month_end_date=date.replace(month=date.month + 1, day=1)
            - timedelta(days=1),
            prev_year_month=str(prev_month),
            prev_month_start_date=date.replace(
                year=prev_year, month=prev_month, day=1
            ),
            prev_month_end_date=date.replace(
                year=prev_year, month=prev_month, day=prev_day
            ),
            quarter=("Q" + str((date.month - 1) // 3 + 1)),
            weekday=date.strftime("%u"),
            week_identifier=date.strftime("%V"),
            year_quarter=date.strftime("%YQ%q"),
            day_of_year=date.timetuple().tm_yday,
            day_of_month=date.day,
            day_of_week=date.weekday() + 1,  # 星期一为1
            week_of_month=((date.day - 1) // 7)
            + 1,  # 当月第几周，星期一为第一周
            week_of_year=date.isocalendar()[1],  # 当年第几周，星期一为第一周
            is_weekend="Yes" if date.weekday() >= 5 else "No",
            date_type=self.__get_date_type(
                date, holiday
            ),  # 需要额外逻辑来确定工作日、休息日、节假日
            holiday_name=holiday.name if holiday else "",  # 计算节假日名称
            hour=hour,
            shift=shift,
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
        for date in iter_days(time_start, time_end):
            date_dimension = self.get_for_date(date)
            date_dimensions.append(date_dimension)

        return date_dimensions


# 辅助函数，用于生成指定日期范围内的所有日期
def iter_days(
    start_date: datetime.date, end_date: datetime.date
) -> Iterator[datetime.date]:
    for n in range((end_date - start_date).days + 1):
        yield start_date + timedelta(days=n)
