from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate

async def crear_ticket(db: AsyncSession, ticket: TicketCreate):
    nuevo = Ticket(**ticket.model_dump())
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo

async def listar_tickets(db: AsyncSession):
    result = await db.execute(select(Ticket))
    return result.scalars().all()

async def actualizar_estado_asignacion(db: AsyncSession, ticket_id: int, estado: str):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    if ticket:
        ticket.estado_asignacion = estado
        await db.commit()
        await db.refresh(ticket)
    return ticket
