import asyncio
from app.database import engine, Base

async def reset_db():
    async with engine.begin() as conn:
        print("⚠️ Eliminando todas las tablas...")
        await conn.run_sync(Base.metadata.drop_all)
        print("🧹 Tablas eliminadas.")

        print("📦 Creando tablas nuevamente...")
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Tablas creadas correctamente.")

if __name__ == "__main__":
    asyncio.run(reset_db())
