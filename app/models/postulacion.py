from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class Postulacion(Base):
    __tablename__ = "postulaciones"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    tecnico_id = Column(Integer, ForeignKey("tecnicos.id"))
    fecha_postulacion = Column(DateTime, default=datetime.utcnow)
    estado = Column(String, default="pendiente")  # ✅ "pendiente", "aceptado", "rechazado"

    ticket = relationship("Ticket", back_populates="postulaciones")
    tecnico = relationship("Tecnico", back_populates="postulaciones")
