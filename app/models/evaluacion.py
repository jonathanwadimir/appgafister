from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Evaluacion(Base):
    __tablename__ = "evaluaciones"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"))
    puntaje = Column(Integer)  # valores esperados entre 1 y 5
    comentario = Column(String, nullable=True)

    ticket = relationship("Ticket", back_populates="evaluacion_rel")
