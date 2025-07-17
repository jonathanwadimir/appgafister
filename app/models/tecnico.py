from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Tecnico(Base):
    __tablename__ = "tecnicos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    zona = Column(String)
    certificado_sec = Column(String)
    emision = Column(String)
