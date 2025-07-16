from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.ticket import Ticket

# Crear ticket
async def create_ticket(db: AsyncSession, ticket: Ticket):
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket

# Obtener tickets por cliente
async def get_tickets_by_cliente(db: AsyncSession, cliente_id: int):
    result = await db.execute(select(Ticket).filter(Ticket.cliente_id == cliente_id))
    return result.scalars().all()

# Obtener ticket por ID
async def get_ticket_by_id(db: AsyncSession, ticket_id: int):
    result = await db.execute(select(Ticket).filter(Ticket.id == ticket_id))
    return result.scalars().first()

# Obtener todos los tickets (con paginación)
async def get_tickets(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Ticket).offset(skip).limit(limit))
    return result.scalars().all()

# Actualizar estado de asignación
async def actualizar_estado_asignacion(db: AsyncSession, ticket: Ticket, nuevo_estado: str):
    ticket.estado_asignacion = nuevo_estado
    await db.commit()
    await db.refresh(ticket)
    return ticket
