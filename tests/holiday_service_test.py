import pytest
import os

from pathlib import Path
from datetime import date
from app.services.holiday_service import HolidayService
from app.schemas.holiday import Holiday


@pytest.fixture
def holiday_service():
    # 指定测试文件路径，确保在测试目录下有此文件
    return HolidayService()


def test_get_for_date_with_holiday_and_is_not_offday(holiday_service):
    # 准备测试数据：假设2023-04-28调休后是工作日
    test_date = date(2024, 4, 28)
    holiday = holiday_service.get_for_date(test_date)

    assert holiday is not None
    assert holiday.date == test_date.strftime("%Y-%m-%d")
    assert holiday.name == "劳动节"
    assert holiday.is_offday == False


def test_get_for_date_with_holiday_and_is_offday(holiday_service):
    # 准备测试数据：假设2024-04-28是调休后是工作日
    test_date = date(2024, 5, 5)
    holiday = holiday_service.get_for_date(test_date)

    assert holiday is not None
    assert holiday.date == test_date.strftime("%Y-%m-%d")
    assert holiday.name == "劳动节"
    assert holiday.is_offday == True


def test_get_for_date_without_holiday(holiday_service):
    # 准备测试数据：假设查询的日期没有节假日
    test_date = date(2024, 1, 2)
    holiday = holiday_service.get_for_date(test_date)

    assert holiday is None


def test_get_for_date_file_not_found():
    service = HolidayService()

    with pytest.raises(FileNotFoundError):
        service.get_for_date(date(2026, 1, 1))
