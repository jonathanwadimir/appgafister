from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import asc
from app.models.postulacion import Postulacion
from app.models.ticket import Ticket
from sqlalchemy.exc import IntegrityError

async def asignar_siguiente_tecnico(db: AsyncSession, ticket_id: int) -> Ticket | None:
    ticket = await db.get(Ticket, ticket_id)
    if not ticket:
        return None

    result = await db.execute(
        select(Postulacion)
        .where(Postulacion.ticket_id == ticket_id)
        .order_by(asc(Postulacion.fecha_postulacion))
    )
    postulaciones = result.scalars().all()
    rechazados = {ticket.tecnico_id} if ticket.tecnico_id else set()

    # También obtener postulaciones rechazadas para no reasignarles
    rechazados.update(
        [p.tecnico_id for p in postulaciones if p.estado == "rechazado"]
    )

    for postulacion in postulaciones:
        if postulacion.tecnico_id not in rechazados and postulacion.estado == "pendiente":
            ticket.tecnico_id = postulacion.tecnico_id
            ticket.estado_asignacion = "pendiente"
            await db.commit()
            await db.refresh(ticket)
            return ticket

    ticket.tecnico_id = None
    ticket.estado_asignacion = "pendiente"
    await db.commit()
    await db.refresh(ticket)
    return ticket

async def crear_postulacion(db: AsyncSession, ticket_id: int, tecnico_id: int) -> Postulacion:
    result = await db.execute(
        select(Postulacion)
        .where(Postulacion.ticket_id == ticket_id)
        .where(Postulacion.tecnico_id == tecnico_id)
    )
    existente = result.scalar_one_or_none()
    if existente:
        raise ValueError("El técnico ya se ha postulado a este ticket.")

    postulacion = Postulacion(ticket_id=ticket_id, tecnico_id=tecnico_id)
    db.add(postulacion)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ValueError("Error al postular: datos inválidos.")
    await db.refresh(postulacion)
    return postulacion

async def obtener_postulaciones_por_ticket(db: AsyncSession, ticket_id: int) -> list[Postulacion]:
    result = await db.execute(
        select(Postulacion).where(Postulacion.ticket_id == ticket_id).order_by(Postulacion.fecha_postulacion)
    )
    return result.scalars().all()

# Nueva función para actualizar estado de postulación
async def actualizar_estado_postulacion(db: AsyncSession, postulacion_id: int, nuevo_estado: str) -> Postulacion | None:
    postulacion = await db.get(Postulacion, postulacion_id)
    if not postulacion:
        return None
    if nuevo_estado not in ("pendiente", "aceptado", "rechazado"):
        raise ValueError("Estado inválido para la postulación.")
    postulacion.estado = nuevo_estado
    await db.commit()
    await db.refresh(postulacion)
    return postulacion
