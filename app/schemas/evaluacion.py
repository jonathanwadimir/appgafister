from pydantic import BaseModel

class EvaluacionBase(BaseModel):
    ticket_id: int
    puntaje: int
    comentario: str

class EvaluacionCreate(EvaluacionBase):
    pass

class EvaluacionOut(EvaluacionBase):
    id: int

    class Config:
        from_attributes = True
