from pydantic import BaseModel, Field
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

    class Config:
        from_attributes = True

class TicketAsignacionUpdate(BaseModel):
    estado_asignacion: str  # aceptado / rechazado

class TicketEvaluacion(BaseModel):
    ticket_id: int = Field(..., description="ID del ticket evaluado")
    calificacion: int = Field(..., ge=1, le=5, description="Calificación del 1 al 5")
    comentario: Optional[str] = Field(None, description="Comentario opcional")

    class Config:
        from_attributes = True
