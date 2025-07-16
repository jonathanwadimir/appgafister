from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.tecnico import Tecnico
from app.schemas import TecnicoCreate



async def create_tecnico(db: AsyncSession, tecnico_data: TecnicoCreate) -> Tecnico:
    tecnico = Tecnico(**tecnico_data.dict())
    db.add(tecnico)
    await db.commit()
    await db.refresh(tecnico)
    return tecnico


async def get_tecnicos(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Tecnico]:
    result = await db.execute(select(Tecnico).offset(skip).limit(limit))
    return result.scalars().all()


async def get_tecnico_by_id(db: AsyncSession, tecnico_id: int) -> Tecnico | None:
    return await db.get(Tecnico, tecnico_id)


async def get_tecnico_by_rut(db: AsyncSession, rut: str) -> Tecnico | None:
    result = await db.execute(select(Tecnico).where(Tecnico.rut == rut))
    return result.scalars().first()
