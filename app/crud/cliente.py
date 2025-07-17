from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate
from sqlalchemy.future import select

async def crear_cliente(db: AsyncSession, cliente: ClienteCreate):
    nuevo = Cliente(**cliente.model_dump())
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo

async def listar_clientes(db: AsyncSession):
    result = await db.execute(select(Cliente))
    return result.scalars().all()
