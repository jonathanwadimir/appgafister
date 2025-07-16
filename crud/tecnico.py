from app.models.tecnico import Tecnico

async def get_tecnico_by_rut(db, rut: str):
    result = await db.execute(
        select(Tecnico).where(Tecnico.rut == rut)
    )
    return result.scalars().first()

async def create_tecnico(db, tecnico: Tecnico):
    db.add(tecnico)
    await db.commit()
    await db.refresh(tecnico)
    return tecnico
