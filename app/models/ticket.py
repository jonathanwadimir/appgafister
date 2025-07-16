from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String)
    multimedia = Column(String, nullable=True)
    emergencia = Column(Boolean, default=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    tecnico_id = Column(Integer, ForeignKey("tecnicos.id"), nullable=True)

    evaluacion = Column(Integer, nullable=True)
    comentario_evaluacion = Column(String, nullable=True)
    estado_asignacion = Column(String, default="pendiente")  # opciones: pendiente, aceptado, rechazado

    cliente = relationship("Cliente", back_populates="tickets")
    tecnico = relationship("Tecnico", back_populates="tickets")
    postulaciones = relationship("Postulacion", back_populates="ticket", cascade="all, delete-orphan")
    
    evaluacion_rel = relationship("Evaluacion", back_populates="ticket", uselist=False, cascade="all, delete-orphan")  # ✅ Relación con modelo Evaluacion
