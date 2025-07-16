from pydantic import BaseModel
from typing import Optional

class TicketBase(BaseModel):
    cliente_id: int
    descripcion: str

class TicketCreate(TicketBase):
    pass

class TicketAsignacionUpdate(BaseModel):
    estado_asignacion: str

class TicketEvaluacion(BaseModel):
    ticket_id: int
    evaluacion: int
    comentario: Optional[str] = None

class TicketOut(TicketBase):
    id: int
    tecnico_id: Optional[int] = None
    estado_asignacion: str
    evaluacion: Optional[int] = None
    comentario_evaluacion: Optional[str] = None

    class Config:
        from_attributes = True
