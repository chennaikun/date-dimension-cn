from datetime import datetime, date
import io

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from csv import writer

from app.controllers.date_dimension_controller import (
    DateDimensionController,
    date_dimension_controller,
)
from app.schemas.date_dimension import DateDimension

date_dimension_router = APIRouter()

# @date_dimension_router.post("/date-dimension")
# async def get_for_date(
#     date: date,
# ) -> DateDimension:
#     try:
#         controller: DateDimensionController = date_dimension_controller(date)
#         return controller.get_for_date(date)
#     except FileNotFoundError as e:
#         raise HTTPException(status_code=404, detail=str(e))


@date_dimension_router.get("/")
def get_ste_day(
    start_date: date,
    end_date: date,
    controller: DateDimensionController = Depends(date_dimension_controller),
) -> list[DateDimension] | None:
    try:
        return controller.get_ste_day(
            datetime.combine(start_date, datetime.min.time()),
            datetime.combine(end_date, datetime.min.time()),
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@date_dimension_router.get("/csv", response_class=StreamingResponse)
def export_to_csv(
    start_date: date,
    end_date: date,
    controller: DateDimensionController = Depends(date_dimension_controller),
) -> StreamingResponse:
    try:
        csv_data = get_ste_day(
            datetime.combine(start_date, datetime.min.time()),
            datetime.combine(end_date, datetime.min.time()),
            controller,
        )
        csv_response = __generate_csv(csv_data)

        return csv_response
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


def __generate_csv(data: list[DateDimension]) -> StreamingResponse:
    """
    生成CSV内容并返回FastAPI的Response对象。
    """
    stream = io.StringIO()
    csv_writer = writer(stream)

    # 动态获取属性名作为表头
    field_names = [
        field_name for field_name in DateDimension.model_fields.keys()
    ]
    csv_writer.writerow(field_names)
    # 写入数据
    for item in data:
        # 使用模型的dict表示形式来遍历属性值
        csv_writer.writerow(
            [str(value) for value in item.model_dump().values()]
        )

    # 获取CSV字符串并设置响应头
    return StreamingResponse(
        content=stream.getvalue(),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=date-dimension.csv"
        },
    )
