import aioredis
from fastapi import FastAPI
import uvicorn
from fastapi_utils.api_model import APIModel

import httpx
import json
import os

# works with redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

app = FastAPI()


# Initialization of FastAPICache on startup event of fastapi
@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


headers = {'X-Yandex-API-Key': os.environ['YANDEX_API_KEY']}


# test camelCase
class Coordinates(APIModel):

    # should accept testCamelCase
    test_camel_case: str = 'It works!'

    lat: str = '59.926815'
    lon: str = '30.339278'


async def get_weather_from_yandex(params):
    print('getting from yandex...')
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.weather.yandex.ru/v2/forecast', params=params, headers=headers)
    return json.load(response)


@app.post("/weather")
@cache(expire=60)
async def weather_from_yandex(coordinates: Coordinates):
    print(coordinates.test_camel_case)
    return await get_weather_from_yandex(coordinates.dict(exclude={'test_camel_case'}))



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
