from pydantic import BaseModel
from typing import Optional
from datetime import date

class TecnicoBase(BaseModel):
    nombre: str
    zona: str
    certificado_sec: Optional[str] = None
    emision: Optional[date] = None

class TecnicoCreate(TecnicoBase):
    pass

class TecnicoRead(TecnicoBase):
    id: int

    class Config:
        from_attributes = True
