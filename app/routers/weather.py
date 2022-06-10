from fastapi import APIRouter, Depends, Query, Path
from app.services.token import get_current_user
from app.services.weather import get_current_weather, get_weather_forecast

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="/weather",
    tags=["weather"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/{fieldId}/yandex/current")
async def current_weather_from_yandex(field_id: str = Path(..., alias='fieldId')):
    return await get_current_weather(field_id)


@router.get("/{fieldId}/yandex/future")
async def weather_forecast_from_yandex(field_id: str = Path(..., alias='fieldId')):
    return await get_weather_forecast(field_id)
