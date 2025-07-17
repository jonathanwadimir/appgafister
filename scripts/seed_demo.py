import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import tecnico, cliente, ticket
from app.crud import tecnico as crud_tecnico, cliente as crud_cliente, ticket as crud_ticket

async def seed():
    async for db in get_db():
        # Clientes demo
        for i in range(3):
            await crud_cliente.crear_cliente(db, cliente.ClienteCreate(
                nombre=f"Cliente{i}", direccion=f"Dirección {i}"
            ))

        # Técnicos demo
        for i in range(3):
            await crud_tecnico.crear_tecnico(db, tecnico.TecnicoCreate(
                nombre=f"Tecnico{i}", zona="Zona Norte", certificado_sec="SEC-0001", emision="2022-01-01"
            ))

        # Tickets demo
        for i in range(3):
            await crud_ticket.crear_ticket(db, ticket.TicketCreate(
                descripcion=f"Fuga de gas {i}", zona="Zona Norte", cliente_id=1
            ))

if __name__ == "__main__":
    asyncio.run(seed())
