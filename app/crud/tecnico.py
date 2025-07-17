from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.tecnico import Tecnico
from app.schemas.tecnico import TecnicoCreate

async def crear_tecnico(db: AsyncSession, tecnico: TecnicoCreate):
    nuevo = Tecnico(**tecnico.model_dump())
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo

async def listar_tecnicos(db: AsyncSession):
    result = await db.execute(select(Tecnico))
    return result.scalars().all()

async def obtener_tecnico_por_id(db: AsyncSession, tecnico_id: int) -> Tecnico | None:
    result = await db.execute(select(Tecnico).where(Tecnico.id == tecnico_id))
    return result.scalar_one_or_none()
