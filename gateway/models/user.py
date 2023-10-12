from pydantic import BaseModel

class User(BaseModel):
    _id: str;
    email: str;
    password: str;