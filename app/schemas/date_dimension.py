from datetime import datetime

from pydantic import BaseModel, Field


class DateDimension(BaseModel):
    """
    DateDimension 类代表了日期维度表中的一个实体，用于存储日期相关的各种属性，
    以便于数据分析、报表生成和时间序列分析等场景。此类利用`pendulum`库来处理日期和时间。
    """

    date: datetime = Field(description="日期，精确到日期的datetime对象")
    date_id: str = Field(
        description="日期ID，格式通常为YYYYMMDDHH，其中HH表示小时"
    )
    date_time: datetime = Field(description="包含时分秒的日期时间")
    prev_year_same_date: datetime = Field(description="去年同一天的日期")
    prev_year_date_id: str = Field(
        description="去年同一天的日期ID，格式YYYYMMDDHH"
    )
    prev_year_date_time: datetime = Field(
        description="去年同一天的完整日期时间"
    )
    year: str = Field(description="当前日期所属的年份，字符串格式")
    year_start_date: datetime = Field(
        description="当年的第一天日期，格式YYYYMMDD"
    )
    prev_year: str = Field(description="去年的年份，字符串格式")
    prev_year_start_date: datetime = Field(
        description="去年的第一天日期，格式YYYYMMDD"
    )
    month: str = Field(description="当前日期所属的月份，字符串格式")
    month_start_date: datetime = Field(
        description="当月的第一天日期，格式YYYYMMDD"
    )
    month_end_date: datetime = Field(
        description="当月的最后一天日期，格式YYYYMMDD"
    )
    prev_year_month: str = Field(description="去年同月的月份，字符串格式")
    prev_month_start_date: datetime = Field(
        description="去年同月的第一天日期，格式YYYYMMDD"
    )
    prev_month_end_date: datetime = Field(
        description="去年同月的最后一天日期，格式YYYYMMDD"
    )
    quarter: str = Field(description="当前日期所属的季度，字符串格式")
    weekday: str = Field(description="星期几，1表示星期一，7表示星期日")
    week_identifier: str = Field(
        description="当前日期所在的一周标识，字符串格式"
    )
    year_quarter: str = Field(
        description="当年的季度标识，格式为YYYYQx，如2023Q1"
    )
    day_of_year: int = Field(description="当前日期在当年的第几天，从1开始")
    day_of_month: int = Field(description="当前日期在当月的第几天")
    day_of_week: int = Field(description="当前日期在当周的第几天，星期一为1")
    week_of_month: int = Field(
        description="当前日期在当月的第几周，星期一作为一周的开始"
    )
    week_of_year: int = Field(
        description="当前日期在当年的第几周，星期一作为一周的开始"
    )
    is_weekend: str = Field(description="指示该日期是否为周末，'Yes'或'No'")
    date_type: str = Field(description="日期类型标识，节假日，工作日，休息日")
    holiday_name: str = Field(description="具体的节假日名称，如果有的话")
    hour: int = Field(description="当前日期的小时，范围为00-23")
    shift: str = Field(
        description="班次标识，0-7表示夜班，8-16表示早班，17-23表示中班"
    )