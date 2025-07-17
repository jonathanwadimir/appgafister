from pydantic import BaseModel

class UsuarioBase(BaseModel):
    rut: str
    rol: str

class UsuarioCreate(UsuarioBase):
    password: str
    nombre: str
    email: str

class UsuarioOut(UsuarioBase):
    id: int
    nombre: str
    email: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    rut: str
