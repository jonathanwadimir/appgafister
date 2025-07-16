from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base

class Tecnico(Base):
    __tablename__ = "tecnicos"

    id = Column(Integer, primary_key=True, index=True)
    rut = Column(String, unique=True, index=True)
    nombre = Column(String)
    zona = Column(String)
    certificado_sec = Column(Boolean)
    emision = Column(String)
    foto_perfil = Column(String)
    acepto_terminos = Column(Boolean)

    tickets = relationship("Ticket", back_populates="tecnico")
    postulaciones = relationship("Postulacion", back_populates="tecnico", cascade="all, delete-orphan")
