from app.database import Base, engine
import asyncio

async def create_all_tables():
    async with engine.begin() as conn:
        # Esto crea todas las tablas definidas en Base.metadata, si no existen
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas o ya existentes.")

if __name__ == "__main__":
    asyncio.run(create_all_tables())
