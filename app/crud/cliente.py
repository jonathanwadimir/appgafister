from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate

async def crear_cliente(db: AsyncSession, cliente: ClienteCreate):
    nuevo = Cliente(**cliente.model_dump())
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo

async def listar_clientes(db: AsyncSession):
    result = await db.execute(select(Cliente))
    return result.scalars().all()

async def get_cliente_by_rut(db: AsyncSession, rut: str) -> Cliente | None:
    result = await db.execute(select(Cliente).where(Cliente.rut == rut))
    return result.scalar_one_or_none()
