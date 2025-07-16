from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.evaluacion import Evaluacion
from app.models.ticket import Ticket
from app.schemas.evaluacion import EvaluacionCreate

async def crear_evaluacion(db: AsyncSession, datos: EvaluacionCreate):
    result = await db.execute(select(Ticket).where(Ticket.id == datos.ticket_id))
    ticket = result.scalar_one_or_none()

    if ticket is None:
        return None, "Ticket no encontrado"

    nueva_eval = Evaluacion(
        ticket_id=datos.ticket_id,
        puntaje=datos.puntaje,
        comentario=datos.comentario
    )

    db.add(nueva_eval)

    # También actualizamos el ticket
    ticket.evaluacion = datos.puntaje
    ticket.comentario_evaluacion = datos.comentario

    await db.commit()
    await db.refresh(nueva_eval)
    return nueva_eval, None
