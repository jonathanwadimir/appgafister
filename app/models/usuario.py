from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    rol = Column(String, nullable=False, default="cliente")  # admin, tecnico, cliente
