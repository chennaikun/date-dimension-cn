import os
import json
import datetime
from functools import lru_cache

from pathlib import Path
import aiofiles

from app.schemas.holiday import Holiday


class HolidayService(object):

    @lru_cache
    async def __load_json(self, date: datetime) -> list[Holiday]:
        """
        按照年份加载节假日json文件
        """
        json_file: Path = self.__get_holiday_json_file(date)
        if not os.path.exists(json_file):
            raise FileNotFoundError

        async with aiofiles.open(json_file) as f:
            contents = await f.read()

        holidays = json.loads(contents)
        return [Holiday(**h) for h in holidays["days"]]

    def __get_holiday_json_file(self, date: datetime) -> Path:
        """build the path of holiday json file

        Args:
            date (datetime): 日期

        Returns:
            Path: json路径
        """
        return Path.cwd() / "holiday-cn" / f"{date.year}.json"

    async def get_for_date(self, date: datetime.date) -> Holiday | None:
        """查询某个日期的节假日

        Args:
            date (datetime.date): 某个日期

        Returns:
            Holiday | None: 节假日。如果没有, 则为None
        """
        holidays = await self.__load_json(date)
        days = [d for d in holidays if d.date == date.strftime("%Y-%m-%d")]

        return days[0] if days else None
