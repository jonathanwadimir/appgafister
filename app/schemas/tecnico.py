from pydantic import BaseModel
from datetime import date

class TecnicoBase(BaseModel):
    nombre: str
    zona: str
    certificado_sec: str
    emision: date

class TecnicoCreate(TecnicoBase):
    pass

class TecnicoOut(TecnicoBase):
    id: int

    class Config:
        from_attributes = True
