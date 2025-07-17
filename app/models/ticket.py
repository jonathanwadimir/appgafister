from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class EstadoAsignacion(str, enum.Enum):
    pendiente = "pendiente"
    aceptado = "aceptado"
    rechazado = "rechazado"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    tecnico_id = Column(Integer, ForeignKey("tecnicos.id"), nullable=True)
    estado_asignacion = Column(Enum(EstadoAsignacion), default=EstadoAsignacion.pendiente)

    cliente = relationship("Cliente")
    tecnico = relationship("Tecnico")
