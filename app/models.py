from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Tecnico(Base):
    __tablename__ = "tecnicos"

    id = Column(Integer, primary_key=True, index=True)
    rut = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    zona_cobertura = Column(String)
    certificado_sec = Column(Boolean, default=False)
    emision_sii = Column(String)  # "Boleta", "Factura", etc.
    foto_perfil_url = Column(String, nullable=True)

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    rut = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    # Otros campos que quieras agregar

    tickets = relationship("Ticket", back_populates="cliente")

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    tecnico_id = Column(Integer, ForeignKey("tecnicos.id"), nullable=True)
    descripcion = Column(Text)
    estado = Column(String, default="pendiente_pool")  # estados según esquema
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    emergencia = Column(Boolean, default=False)
    multimedia = Column(String)  # URL o JSON con imágenes
    # ... otros campos como tecnico_id, score_cliente, etc.

    cliente = relationship("Cliente", back_populates="tickets")
