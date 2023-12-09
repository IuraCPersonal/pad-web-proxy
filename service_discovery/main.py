import httpx
import json
from fastapi import FastAPI, status, Response
from fastapi.encoders import jsonable_encoder

app = FastAPI()

auth_service_replicas = []
reservations_service_replicas = []

status_codes = {
    200: 0,
    400: 0,
    304: 0,
    404: 0,
    500: 0
}

class Service():
    serviceType: str
    serviceHost: str
    servicePort: int

@app.middleware("http")
async def count_status_codes(request, call_next):
    response = await call_next(request)
    if request.url.path != '/metrics':
        status_codes[response.status_code] = status_codes.get(response.status_code, 0) + 1
    return response

@app.get(
    "/api/v1/status",
    tags=["healthcheck", "status"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def status():
    return {"status": "OK"}


@app.post(
    "/services",
    tags=["register"],
)
async def register(service):
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
)
async def get_replicas():
    return Response(    
        content=json.dumps({
            "auth": [{
                "host": "auth",
                "port": "3001" 
            }],
            "reservations": [{
                "host": "reservations",
                "port": "3009"
            }]
        }),
        media_type="application/json"
    )

@app.get('/metrics')
async def metrics():
    metrics_text = [
        '# HELP http_requests_total The total number of HTTP requests.',
        '# TYPE http_requests_total counter'
    ]
    for key, value in status_codes.items():
        metrics_text.append(f'http_requests_total{{code="{key}"}} {value}')
    return "\n".join(metrics_text)

@app.get('/status')
async def status():
    return {"status": "OK"}
