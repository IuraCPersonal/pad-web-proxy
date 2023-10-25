import httpx
import json
from fastapi import FastAPI, status, Response
from fastapi.encoders import jsonable_encoder

from models.index import *

app = FastAPI()

auth_service_replicas = []
reservations_service_replicas = []


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
    "/services",
    tags=["register"],
)
async def register(service: Service):
    if (not service.name or not service.port or not service.host):
        return status.HTTP_400_BAD_REQUEST

    new_service = {
        "host": service.host,
        "port": service.port
    }

    if (service.type == 'auth'):
        auth_service_replicas.append(new_service)
    elif (service.type == 'reservations'):
        reservations_service_replicas.append(new_service)
    else:
        return status.HTTP_400_BAD_REQUEST

    return status.HTTP_201_CREATED


@app.get(
    "/services",
    tags=["register"],
    status_code=status.HTTP_200_OK
)
async def get_replicas():
    return Response(
        content=json.dumps({
            "auth": auth_service_replicas,
            "reservations": reservations_service_replicas
        }),
        media_type="application/json"
    )
