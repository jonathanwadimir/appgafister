from pydantic import BaseModel

class UsuarioBase(BaseModel):
    username: str
    rol: str

class UserCreate(UsuarioBase):  # Cambiado a UserCreate para que coincida con router
    password: str

class UserOut(UsuarioBase):  # Cambiado a UserOut
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
