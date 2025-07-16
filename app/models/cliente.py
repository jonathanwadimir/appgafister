from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    rut = Column(String, unique=True, index=True)
    nombre = Column(String)
    direccion = Column(String)
    telefono = Column(String)

    # Relación con los tickets
    tickets = relationship("Ticket", back_populates="cliente")
