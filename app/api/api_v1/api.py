from fastapi import APIRouter

from app.api.api_v1.endpoints.date_dimension import date_dimension_router
from app.api.api_v1.endpoints.holiday import holiday_router

api_router = APIRouter()

api_router.include_router(holiday_router, prefix="/holiday", tags=["holiday"])
api_router.include_router(
    date_dimension_router, prefix="/date_dimension", tags=["date_dimension"]
)
