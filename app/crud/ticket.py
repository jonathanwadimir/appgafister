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

async def get_tickets(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Ticket).offset(skip).limit(limit))
    return result.scalars().all()

async def get_ticket_by_id(db: AsyncSession, ticket_id: int):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    return result.scalar_one_or_none()

async def actualizar_estado_asignacion(db: AsyncSession, ticket_id: int, estado: str):
    ticket = await get_ticket_by_id(db, ticket_id)
    if ticket:
        ticket.estado_asignacion = estado
        await db.commit()
        await db.refresh(ticket)
    return ticket

async def get_tickets_by_cliente(db: AsyncSession, cliente_id: int):
    result = await db.execute(select(Ticket).where(Ticket.cliente_id == cliente_id))
    return result.scalars().all()

async def asignar_siguiente_tecnico(db: AsyncSession, ticket_id: int):
    # Implementa aquí la lógica para reasignar a otro técnico automáticamente
    ticket = await get_ticket_by_id(db, ticket_id)
    return ticket
