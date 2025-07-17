from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class EstadoPostulacion(str, enum.Enum):
    pendiente = "pendiente"
    aceptado = "aceptado"
    rechazado = "rechazado"

class Postulacion(Base):
    __tablename__ = "postulaciones"

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    tecnico_id = Column(Integer, ForeignKey("tecnicos.id"))
    estado = Column(Enum(EstadoPostulacion), default=EstadoPostulacion.pendiente)

    ticket = relationship("Ticket", backref="postulaciones")
    tecnico = relationship("Tecnico")
