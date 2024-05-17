import pytest
from datetime import datetime, timedelta
import pendulum

from app.services.holiday_service import HolidayService
from app.services.date_dimension_service import DateDimensionService
from app.schemas.date_dimension import DateDimension
from app.schemas.holiday import Holiday


@pytest.fixture
def date_dim_service():
    holiday_service = HolidayService()
    service = DateDimensionService(holiday_service)

    return service


def test_get_for_date_normal_workday(date_dim_service):
    test_date = pendulum.datetime(
        2024, 4, 5, tz="UTC"
    )  # 任意正常工作日日期时间

    expected_date_id = test_date.strftime("%Y%m%d%H")
    expected_year = str(test_date.year)
    expected_month = str(test_date.month)
    expected_weekday = test_date.strftime("%u")
    expected_week_identifier = test_date.strftime("%a")
    expected_year_quarter = test_date.strftime("%YQ") + str(
        (test_date.month - 1) // 3 + 1
    )
    expected_day_of_year = test_date.timetuple().tm_yday
    expected_day_of_month = test_date.day
    expected_day_of_week = test_date.weekday() + 1
    expected_week_of_month = ((test_date.day - 1) // 7) + 1
    expected_week_of_year = test_date.isocalendar()[1]
    expected_is_weekend = "No" if test_date.weekday() < 5 else "Yes"
    expected_hour = str(test_date.hour)
    expected_shift = (
        "早"
        if test_date.hour < 17 and test_date.hour > 8
        else "夜" if test_date.hour < 8 else "中"
    )
    expected_holiday_name = "清明节"
    expected_date_type = "节假日"

    results = date_dim_service.get_for_date(test_date)
    result = results[0]
    assert len(results) == 24
    assert isinstance(result, DateDimension)
    assert result.date == test_date
    assert result.date_hour_id == expected_date_id
    assert result.year == expected_year
    assert result.month == expected_month
    assert result.weekday == expected_weekday
    assert result.week_identifier == expected_week_identifier
    assert result.year_quarter == expected_year_quarter
    assert result.day_of_year == expected_day_of_year
    assert result.day_of_month == expected_day_of_month
    assert result.day_of_week == expected_day_of_week
    assert result.week_of_month == expected_week_of_month
    assert result.week_of_year == expected_week_of_year
    assert result.is_weekend == expected_is_weekend
    assert result.hour == expected_hour
    assert result.shift == expected_shift
    assert result.holiday_name == expected_holiday_name
    assert result.date_type == expected_date_type


def test_get_for_date_weekend(date_dim_service):
    test_date = datetime(2024, 4, 7, 12, 0, 0)  # 周末日期时间

    expected_date_hour_id = test_date.strftime("%Y%m%d%H")
    expected_is_weekend = "Yes"

    result = date_dim_service.get_for_date(test_date)[12]

    assert result.is_weekend == expected_is_weekend
    assert result.date_hour_id == expected_date_hour_id


def test_get_for_date_holiday_is_not_offday(date_dim_service):
    test_date = datetime(2024, 4, 28, 12, 0, 0)  # 公共假期日期时间

    expected_date_hour_id = test_date.strftime("%Y%m%d%H")
    expected_holiday_name = "劳动节"
    expected_date_type = "工作日"

    result = date_dim_service.get_for_date(test_date)[12]

    assert result.holiday_name == expected_holiday_name
    assert result.date_type == expected_date_type
    assert result.date_hour_id == expected_date_hour_id


def test_get_for_date_holiday_is_offday(date_dim_service):
    test_date = datetime(2024, 5, 5, 12, 0, 0)  # 公共假期日期时间

    expected_date_hour_id = test_date.strftime("%Y%m%d%H")
    expected_holiday_name = "劳动节"
    expected_date_type = "节假日"

    result = date_dim_service.get_for_date(test_date)[12]

    assert result.holiday_name == expected_holiday_name
    assert result.date_type == expected_date_type
    assert result.date_hour_id == expected_date_hour_id


def test_get_for_date_night_shift(date_dim_service):
    test_date = datetime(2024, 4, 6, 1, 0, 0)  # 夜班日期时间

    expected_shift = "夜"

    result = date_dim_service.get_for_date(test_date)[1]

    assert result.shift == expected_shift


def test_get_for_date_morning_shift(date_dim_service):
    test_date = datetime(2024, 4, 6, 9, 0, 0)  # 早班日期时间

    expected_shift = "早"

    result = date_dim_service.get_for_date(test_date)[9]

    assert result.shift == expected_shift
