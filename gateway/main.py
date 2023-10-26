import os

import httpx
import redis

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from pybreaker import CircuitBreaker, CircuitRedisStorage, STATE_CLOSED

from models.user import User
from models.health import HealthCheck

app = FastAPI()

redis = redis.StrictRedis()
db_breaker = CircuitBreaker(
    fail_max=5,
    reset_timeout=60,
    state_storage=CircuitRedisStorage(STATE_CLOSED, redis)
)

REDIS_HOST = os.getenv('REDIS_HOST') or "redis-cache"
REDIS_PORT = os.getenv('REDIS_PORT') or 6379


def cache():
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT
    )


@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
async def get_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")


@app.post(
    "/users"
)
async def create_user(new_user):
    return 201


@app.post(
    "/auth/login"
)
async def login(credentials):
    return 200


@app.get(
    "/reservations"
)
async def get_reservations():
    return 200


@app.post(
    "/reservations"
)
async def create_reservation(new_reservation):
    return 201


@app.get(
    "/reservations/{reservation_id}"
)
async def get_reservation_details():
    return 200
