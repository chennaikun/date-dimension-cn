from datetime import datetime, date
import io
from typing import Generator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from csv import writer

from app.controllers.date_dimension_controller import (
    DateDimensionController,
    date_dimension_controller,
)
from app.schemas.date_dimension import DateDimension

date_dimension_router = APIRouter()


@date_dimension_router.get("/date")
async def get_for_date(
    date: date,
    controller: DateDimensionController = Depends(date_dimension_controller),
) -> list[DateDimension]:
    try:
        return await controller.get_for_date(date)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@date_dimension_router.get("/")
async def get_ste_day(
    start_date: date,
    end_date: date,
    controller: DateDimensionController = Depends(date_dimension_controller),
) -> list[DateDimension] | None:
    try:
        return await controller.get_ste_day(
            datetime.combine(start_date, datetime.min.time()),
            datetime.combine(end_date, datetime.min.time()),
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@date_dimension_router.get("/csv", response_class=StreamingResponse)
async def export_to_csv(
    start_date: date,
    end_date: date,
    controller: DateDimensionController = Depends(date_dimension_controller),
) -> StreamingResponse:
    try:
        return StreamingResponse(
            content=controller.generate_csv(start_date, end_date),
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=date-dimension.csv"
            },
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
