from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.cliente import Cliente
from app.schemas import ClienteCreate
from typing import List, Optional


async def create_cliente(db: AsyncSession, cliente_data: ClienteCreate) -> Cliente:
    cliente = Cliente(**cliente_data.model_dump())
    db.add(cliente)
    await db.commit()
    await db.refresh(cliente)
    return cliente


async def get_cliente_by_rut(db: AsyncSession, rut: str) -> Optional[Cliente]:
    result = await db.execute(select(Cliente).where(Cliente.rut == rut))
    return result.scalars().first()


async def get_clientes(db: AsyncSession) -> List[Cliente]:
    result = await db.execute(select(Cliente))
    return result.scalars().all()
