import os
import time
import json
import httpx
import redis
import logging
import asyncio
import functools

from datetime import datetime
from httpx import ConnectError
from fastapi import FastAPI, HTTPException, status, Depends

from models.user import User
from models.health import HealthCheck

MAX_RETRIES = 3
TASK_TIMEOUT_MS = 1000
MAX_REROUTES = 3

################ LOGGING ################

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

################ REDIS ################

from rediscluster import RedisCluster
import atexit

startup_nodes = [
    {"host": "redis-node-1", "port": "7000"},
    {"host": "redis-node-2", "port": "7001"},
    {"host": "redis-node-3", "port": "7002"},
    {"host": "redis-node-4", "port": "7003"},
    {"host": "redis-node-5", "port": "7004"},
    {"host": "redis-node-6", "port": "7005"},
]

try:
    redis_client = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
    print("Connected to Redis")
except Exception as err:
    print(f"Error connecting to Redis: {err}")

def close_redis():
    redis_client.close()
    print("Redis client is closed")

atexit.register(close_redis)

################ CIRCUIT BREAKER ################

async def circuit_breaker(service_type: str, service_url: str):
    start = datetime.now()
    errors = 0

    while True:
        try:
            async with httpx.AsyncClient() as client:
                await client.get(f"{service_url}/status")
        except (httpx.ConnectError, httpx.HTTPError) as error:
            errors += 1

            if errors >= 3 and (datetime.now() - start).total_seconds() * 1000 <= TASK_TIMEOUT_MS * 3.5:
                print(f"CIRCUIT BREAKER: Service of type {service_type} located at {service_url} is UNHEALTHY!!!")
                return

            continue

        break

# Run the circuit breaker function in the background
asyncio.create_task(circuit_breaker("service_type", "service_url"))

################ LOAD BALANCER ################

reservations_service_counter = 0
payments_service_counter = 0

async def call_service(service_type: str, request_method: str, request_url: str, req_body: dict):
    global reservations_service_counter, payments_service_counter

    service_discovery_response = httpx.get("http://service-discovery:7777/services")
    
    print(service_discovery_response.json())


    reservations_services = service_discovery_response.json()["reservations"]
    payments_services = service_discovery_response.json()["auth"]

    for _ in range(MAX_REROUTES):
        reservations_service_counter = reservations_service_counter % len(reservations_services)
        payments_service_counter = payments_service_counter % len(payments_services)

        if service_type == 'reservations':
            next_service = reservations_services[reservations_service_counter]
            reservations_service_counter += 1
        elif service_type == 'auth':
            next_service = payments_services[payments_service_counter]
            payments_service_counter += 1

        host, port = next_service["host"], next_service["port"]
        next_service_url = f"http://{host}:{port}"

        try:
            print(f"Attempting call to service of type {service_type} at {next_service_url}")
            service_response = httpx.request(
                method=request_method,
                url=f"{next_service_url}/{request_url}",
                json=req_body
            )
            return {"statusCode": 200, "responseBody": service_response.json(), "serviceUrl": next_service_url}
        except (httpx.ConnectError, httpx.HTTPError) as error:
            print(f"Failed to call service of type {service_type} at {next_service_url}")
            await circuit_breaker(service_type, next_service_url)
            continue

    return {"statusCode": 500, "responseBody": {"message": f"{service_type} Service Call Failed"}}

################ SERVICE ################


app = FastAPI()


@app.get(
    "/api/v1/status",
    tags=["healthcheck", "status"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
async def status() -> HealthCheck:
    return {"status": "OK"}


@app.post("/api/v1/users")
async def register_user(user: User):
    response = await call_service('auth', 'post', 'api/users', user.dict())
    if response["statusCode"] != 200:
        raise HTTPException(status_code=response["statusCode"], detail=response["responseBody"])
    return response["responseBody"]

@app.post("/api/v1/auth/login")
async def login_user(user: User):
    response = await call_service('auth', 'post', 'api/auth/login', user.dict())
    if response["statusCode"] != 200:
        raise HTTPException(status_code=response["statusCode"], detail=response["responseBody"])
    return response["responseBody"]

@app.get("/api/v1/reservations")
async def get_reservations():
    response = await call_service('reservations', 'get', 'api/reservations', {})
    if response["statusCode"] != 200:
        raise HTTPException(status_code=response["statusCode"], detail=response["responseBody"])
    return response["responseBody"]

@app.post("/api/v1/reservations")
async def create_reservation(reservation):
    response = await call_service('reservations', 'post', 'api/reservations', reservation.dict())
    if response["statusCode"] != 200:
        raise HTTPException(status_code=response["statusCode"], detail=response["responseBody"])
    
    if response["statusCode"] == 200:
        await redis_client.set(f'api/reservations', '')
        if reservation is not None:
            await redis_client.set(f'api/reservations', '')
    
    return response["responseBody"]