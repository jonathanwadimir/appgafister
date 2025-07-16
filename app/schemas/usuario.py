from pydantic import BaseModel
from typing import Literal

class UserCreate(BaseModel):
    username: str
    password: str
    rol: Literal["admin", "tecnico", "cliente"] = "cliente"

class UserOut(BaseModel):
    id: int
    username: str
    rol: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
