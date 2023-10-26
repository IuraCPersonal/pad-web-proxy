from pydantic import BaseModel


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"


class Service(BaseModel):
    name: str
    type: str
    host: str
    port: int
