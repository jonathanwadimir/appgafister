import asyncio
from app.database import engine, Base

async def drop_all_tables():
    async with engine.begin() as conn:
        print("⚠️ Eliminando todas las tablas...")
        await conn.run_sync(Base.metadata.drop_all)
        print("✅ Todas las tablas han sido eliminadas.")

if __name__ == "__main__":
    asyncio.run(drop_all_tables())
