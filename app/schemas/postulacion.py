from pydantic import BaseModel
from typing import Optional

class PostulacionCreate(BaseModel):
    tecnico_id: int
    ticket_id: int
    puntaje: Optional[int] = None

class PostulacionOut(PostulacionCreate):
    id: int

    class Config:
        from_attributes = True
from pydantic import BaseModel

class PostulacionBase(BaseModel):
    ticket_id: int
    tecnico_id: int

class PostulacionCreate(PostulacionBase):
    pass

class PostulacionOut(PostulacionBase):
    id: int
    estado: str

    class Config:
        from_attributes = True
