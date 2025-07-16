from pydantic import BaseModel, Field

class EvaluacionBase(BaseModel):
    puntaje: int = Field(ge=1, le=5)
    comentario: str | None = None

class EvaluacionCreate(EvaluacionBase):
    ticket_id: int

class EvaluacionOut(EvaluacionBase):
    id: int
    ticket_id: int

    class Config:
        from_attributes = True
