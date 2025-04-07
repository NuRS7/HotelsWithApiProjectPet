import time

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from sqladmin import Admin

from admin.auth import authentication_backend
from admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from bookings.router import router as router_bookings
from config import settings
from database import engine
from hotels.router import router as router_hotels
from images.router import router as router_images
from importer.router import router as router_import
from logger import logger
from pages.router import router as router_pages
from prometheus.router import router as router_prometheus
from users.router import router_auth, router_users

app = FastAPI(
    title="Hotels",
    version="0.1.0",
    root_path="/api",
)


if settings.MODE != "TEST":
    # Подключение Sentry для мониторинга ошибок. Лучше выключать на период локального тестирования
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
    )


# Включение основных роутеров
app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_bookings)

# Включение дополнительных роутеров
app.include_router(router_images)
app.include_router(router_prometheus)
app.include_router(router_import)


origins = [
    "http://localhost",  # Adjust based on where your frontend is served from
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    # Example: If your frontend and backend are served from different ports
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/api/v{major}",
)

app.include_router(router_pages)

if settings.MODE == "TEST":

    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")


@app.on_event("startup")
def startup():
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)


admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(BookingsAdmin)

app.mount("/static", StaticFiles(directory="static"), "static")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # При подключении Prometheus + Grafana подобный лог не требуется
    logger.info("Request handling time", extra={"process_time": round(process_time, 4)})
    return response
