from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketBase(BaseModel):
    descripcion: str
    zona: str
    cliente_id: int

class TicketCreate(TicketBase):
    pass

class TicketOut(TicketBase):
    id: int
    tecnico_id: Optional[int]
    estado_asignacion: str
    creado_en: datetime
    evaluacion: Optional[int] = None
    comentario_evaluacion: Optional[str] = None

    class Config:
        from_attributes = True

class TicketAsignacionUpdate(BaseModel):
    estado_asignacion: str  # Ej: "aceptado" o "rechazado"

class TicketEvaluacion(BaseModel):
    ticket_id: int
    evaluacion: int  # puntuación (por ejemplo 1-5)
    comentario: Optional[str]
