from pydantic import BaseModel
from typing import Optional, Literal

# ----------- TÉCNICO -----------
class TecnicoCreate(BaseModel):
    nombre: str
    rut: str
    certificado_sec: bool
    foto_perfil: Optional[str] = None
    zona: str
    emision: str
    acepto_terminos: bool

class TecnicoOut(TecnicoCreate):
    id: int

    class Config:
        from_attributes = True

# ----------- CLIENTE -----------
class ClienteCreate(BaseModel):
    rut: str
    nombre: str

class ClienteOut(ClienteCreate):
    id: int

    class Config:
        from_attributes = True

# ----------- TICKET -----------
class TicketCreate(BaseModel):
    cliente_id: int
    descripcion: str
    multimedia: Optional[str] = None
    emergencia: bool = False

class TicketOut(TicketCreate):
    id: int
    tecnico_id: Optional[int]

    class Config:
        from_attributes = True

class TicketRead(TicketOut):
    evaluacion: Optional[int] = None
    comentario_evaluacion: Optional[str] = None
    estado_asignacion: Optional[str] = None

    class Config:
        from_attributes = True

class TicketEvaluacion(BaseModel):
    ticket_id: int
    evaluacion: int
    comentario: Optional[str] = None
    recomendaria: Optional[bool] = None

class TicketAsignacionUpdate(BaseModel):
    estado_asignacion: Literal["aceptado", "rechazado"]

# ----------- AUTENTICACIÓN -----------
class UserCreate(BaseModel):
    username: str
    password: str
    rol: Optional[str] = "cliente"

class UserOut(BaseModel):
    id: int
    username: str
    rol: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    rol: Optional[str] = None  # ✅ necesario para validación de rol

# ----------- POSTULACIÓN -----------
class PostulacionBase(BaseModel):
    ticket_id: int
    tecnico_id: int

class PostulacionCreate(PostulacionBase):
    pass

class PostulacionOut(PostulacionBase):
    id: int

    class Config:
        from_attributes = True
