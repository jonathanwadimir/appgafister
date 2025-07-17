from sqlalchemy import Column, Integer, ForeignKey, String
from app.models.base import Base

class Evaluacion(Base):
    __tablename__ = "evaluaciones"

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    puntuacion = Column(Integer)
    comentario = Column(String, nullable=True)
