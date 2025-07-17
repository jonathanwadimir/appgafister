from sqlalchemy.ext.asyncio import AsyncSession
from app.models.evaluacion import Evaluacion
from app.schemas.evaluacion import EvaluacionCreate

async def crear_evaluacion(db: AsyncSession, evaluacion: EvaluacionCreate):
    nueva = Evaluacion(**evaluacion.model_dump())
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva

async def obtener_evaluacion_por_ticket(db: AsyncSession, ticket_id: int):
    result = await db.execute(
        select(Evaluacion).where(Evaluacion.ticket_id == ticket_id)
    )
    return result.scalar_one_or_none()
