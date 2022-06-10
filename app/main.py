import aioredis
from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.routers import (
    auth,
    users,
    settings,
    notification,
    problems,
    files,
    fields,
    weather,
    monitoring
)

app = FastAPI(
              title="AEROSPACE-AGRO",
              version=" 0.0.9")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:3000",
    "https://develop.d35vtbev8rw8ix.amplifyapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/v1")
app.include_router(users.router, prefix="/v1")
app.include_router(settings.router, prefix="/v1")
app.include_router(notification.router, prefix="/v1")
app.include_router(problems.router, prefix="/v1")
app.include_router(files.router, prefix="/v1")
app.include_router(fields.router, prefix="/v1")
app.include_router(weather.router, prefix="/v1")
app.include_router(monitoring.router, prefix="/v1")


# Initialization of FastAPICache on startup event of fastapi
@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get("/")
async def root(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}


@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}
