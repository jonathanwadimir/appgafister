from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.postulacion import Postulacion
from app.schemas.postulacion import PostulacionCreate

async def crear_postulacion(db: AsyncSession, postulacion: PostulacionCreate):
    nueva = Postulacion(**postulacion.model_dump())
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva

async def obtener_postulaciones_por_ticket(db: AsyncSession, ticket_id: int):
    result = await db.execute(select(Postulacion).where(Postulacion.ticket_id == ticket_id))
    return result.scalars().all()

async def actualizar_estado_postulacion(db: AsyncSession, postulacion_id: int, estado: str):
    result = await db.execute(select(Postulacion).where(Postulacion.id == postulacion_id))
    postulacion = result.scalar_one_or_none()
    if postulacion:
        postulacion.estado = estado
        await db.commit()
        await db.refresh(postulacion)
    return postulacion

# Función para asignar siguiente técnico postulado (ejemplo básico)
async def asignar_siguiente_tecnico_postulado(db: AsyncSession, ticket_id: int):
    # Aquí deberías implementar la lógica para obtener el siguiente técnico postulado
    # que aún no haya sido rechazado, o según criterios específicos.
    result = await db.execute(
        select(Postulacion)
        .where(Postulacion.ticket_id == ticket_id)
        .where(Postulacion.estado == "postulado")  # solo postulaciones activas
        .order_by(Postulacion.id)
    )
    siguiente = result.scalars().first()
    return siguiente
