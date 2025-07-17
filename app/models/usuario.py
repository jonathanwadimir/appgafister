from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    rut = Column(String, unique=True, index=True, nullable=False)  # Login con rut
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    rol = Column(String, nullable=False)
