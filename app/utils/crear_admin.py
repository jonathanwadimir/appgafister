from app.database import AsyncSessionLocal
from app.models.usuario import Usuario
from app.utils.hash import get_password_hash

async def crear_usuario_admin():
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            Usuario.__table__.select().where(Usuario.username == "admin")
        )
        existing_user = result.first()
        if not existing_user:
            nuevo = Usuario(
                username="admin",
                hashed_password=get_password_hash("admin123")
            )
            db.add(nuevo)
            await db.commit()
            print("🟢 Usuario admin creado.")
        else:
            print("🟡 Usuario admin ya existe.")
