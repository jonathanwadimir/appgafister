from pydantic import BaseModel

class ClienteBase(BaseModel):
    nombre: str
    correo: str

class ClienteCreate(ClienteBase):
    pass

class ClienteOut(ClienteBase):
    id: int

    class Config:
        from_attributes = True
