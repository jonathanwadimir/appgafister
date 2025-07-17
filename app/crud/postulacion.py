from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.postulacion import Postulacion
from app.models.ticket import Ticket
from app.schemas.postulacion import PostulacionCreate

async def crear_postulacion(db: AsyncSession, postulacion: PostulacionCreate):
    nueva = Postulacion(**postulacion.model_dump())
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva

async def listar_postulaciones(db: AsyncSession):
    result = await db.execute(select(Postulacion))
    return result.scalars().all()

async def actualizar_estado_postulacion(db: AsyncSession, postulacion_id: int, estado: str):
    result = await db.execute(select(Postulacion).where(Postulacion.id == postulacion_id))
    postulacion = result.scalar_one_or_none()
    if postulacion:
        postulacion.estado = estado
        await db.commit()
        await db.refresh(postulacion)
    return postulacion
