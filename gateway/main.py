import httpx
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pybreaker import CircuitBreaker, CircuitBreakerError

from models.user import User
from models.health import HealthCheck

app = FastAPI()

# Create a Circuit Breaker
circuit_breaker = CircuitBreaker(
    fail_max=3,   # Maximum number of consecutive failures before opening the circuit
    reset_timeout=30,  # Time in seconds to wait before attempting to close the circuit again
)


@app.exception_handler(CircuitBreakerError)
async def handle_circuit_breaker_error(request, exc):
    return JSONResponse(content={"error": "Circuit is open"}, status_code=503)


@app.get("/simulate-failure")
def simulate_failure(status_code=status.HTTP_503_SERVICE_UNAVAILABLE):
    return status.HTTP_503_SERVICE_UNAVAILABLE


@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
@circuit_breaker
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
