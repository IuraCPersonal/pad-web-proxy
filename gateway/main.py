import httpx
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

from models.user import User

app = FastAPI()

reservations = "http://localhost:3000"
auth = "http://localhost:3001"

headers = {"Content-Type": "application/json"}


class JWT:
    def __init__(self):
        self.token = ""

    def set(self, payload: str):
        self.token = payload

    def get(self):
        return self.token


token = JWT()


@app.get("/reservations")
async def health():
    r = httpx.get(f"{reservations}")

    return r.json()


@app.get("/reservations/reservations")
async def get_reservations():
    r = httpx.get(f"{reservations}/reservations",
                  cookies={"Authentication": token.get()})

    return r.json()


@app.post("/auth/login", response_model=User)
async def get(payload: User):
    r = httpx.post(f"{auth}/auth/login",
                   json=jsonable_encoder(payload), headers=headers)
    token.set(r.cookies.get("Authentication"))

    return r.json()
