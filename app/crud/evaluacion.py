from sqlalchemy.ext.asyncio import AsyncSession
from app.models.evaluacion import Evaluacion
from app.schemas.evaluacion import EvaluacionCreate

async def crear_evaluacion(db: AsyncSession, evaluacion: EvaluacionCreate):
    nueva = Evaluacion(**evaluacion.model_dump())
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva
