import json
import httpx
import os

from app.db.crud import get_field_coordinates
from app.schemas.coordinates import Coordinates

headers = {'X-Yandex-API-Key': os.environ['YANDEX_API_KEY']}


def __convert_coordinates__(coordinates):
    # X Average
    lat = (coordinates[0][0] + coordinates[1][0] + coordinates[2][0] + coordinates[3][0]) / 4
    # Y Average
    lon = (coordinates[0][1] + coordinates[1][1] + coordinates[2][1] + coordinates[4][1]) / 4
    return lat, lon


def get_coordinates(field_id: str):
    coordinates = __convert_coordinates__(get_field_coordinates(field_id))
    coordinates = Coordinates(lat=coordinates[0], lon=coordinates[1])
    return coordinates


async def get_weather_from_yandex(field_id: str):
    params = get_coordinates(field_id).dict()
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.weather.yandex.ru/v2/forecast', params=params, headers=headers)
    print(response)
    return response


async def get_current_weather(field_id: str):
    response = await get_weather_from_yandex(field_id)
    return json.load(response)["fact"]
    # return {"fact": json.load(response)["fact"], "forecasts": json.load(response)["forecasts"][0]}


async def get_weather_forecast(field_id: str):
    response = await get_weather_from_yandex(field_id)
    return json.load(response)["forecasts"][1:]


if __name__ == '__main__':
    '''print(get_weather("5b265908-9593-4c4e-99f3-8b00d81b64cb"))'''
