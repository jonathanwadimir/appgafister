from pydantic import BaseModel
from datetime import datetime

class PostulacionBase(BaseModel):
    tecnico_id: int
    ticket_id: int

class PostulacionCreate(PostulacionBase):
    pass

class PostulacionOut(PostulacionBase):
    id: int
    estado: str
    postulacion_en: datetime

    class Config:
        from_attributes = True

class PostulacionEstadoUpdate(BaseModel):
    estado: str
