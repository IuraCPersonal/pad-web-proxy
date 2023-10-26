import os
import json
import httpx
import redis
import logging
import functools
import datetime

from httpx import ConnectError
from fastapi import FastAPI, HTTPException, status, Depends

from models.user import User
from models.health import HealthCheck

################ LOGGING ################

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

################ REDIS ################


def create_redis():
    return redis.ConnectionPool(
        host="redis-cache",
        port=6379,
        db=0,
        decode_responses=True
    )


pool = create_redis()


def cache():
    return redis.Redis(connection_pool=pool)

################ LOAD BALANCER ################


reservations_service_counter = 0
payments_service_counter = 0


def getNextReservationsReplica():
    global reservations_service_counter
    replicas = httpx.get('http://service-discovery:7777/services').json()

    targets = replicas["reservations"]

    print(targets)

    reservations_service_counter = reservations_service_counter % len(targets)
    next_service = targets[reservations_service_counter]
    reservations_service_counter += 1

    return f"http://{next_service['host']}:{next_service['port']}"

################ SERVICE ################


app = FastAPI()


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
async def get_reservations(
    redis_client: cache = Depends(cache),
):
    try:
        if (cached_reservations := redis_client.get("reservations")) is not None:
            return json.loads(cached_reservations)

        instance_url = getNextReservationsReplica()

        res = httpx.get(instance_url + "/reservations")

        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail=res.text)

        redis_client.set("reservations", json.dumps(
            res.json()), ex=datetime.timedelta(minutes=1))

        return res.json()
    except ConnectError:
        raise HTTPException(status_code=500, detail="Request timeout.")


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
