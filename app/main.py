from fastapi import FastAPI
from app.database import engine
from app.models.base import Base
from app.routers import tecnico, cliente, ticket, postulacion, evaluacion, usuario, auth
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.usuario import UsuarioCreate
from app.crud import usuario as crud_usuario

app = FastAPI(
    title="Sistema de Tickets Técnicos",
    description="API para gestión de técnicos, clientes y tickets con integración Telegram",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth, prefix="/auth", tags=["Autenticación"])
app.include_router(usuario, prefix="/usuarios", tags=["Usuarios"])
app.include_router(tecnico, prefix="/tecnicos", tags=["Técnicos"])
app.include_router(cliente, prefix="/clientes", tags=["Clientes"])
app.include_router(ticket, prefix="/tickets", tags=["Tickets"])
app.include_router(postulacion, prefix="/postulaciones", tags=["Postulaciones"])
app.include_router(evaluacion, prefix="/evaluaciones", tags=["Evaluaciones"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Crear usuario admin si no existe
    async with AsyncSession(engine) as session:
        admin_rut = "admin1"
        admin_password = "admin"
        admin_rol = "admin"

        existing_user = await crud_usuario.obtener_usuario_por_rut(session, admin_rut)
        if not existing_user:
            nuevo_usuario = UsuarioCreate(
                rut=admin_rut,
                password=admin_password,
                nombre="Administrador",
                email="admin@example.com",
                rol=admin_rol
            )
            await crud_usuario.crear_usuario(session, nuevo_usuario)
            print(f"✅ Usuario administrador creado automáticamente: {admin_rut}")
        else:
            print(f"ℹ️ Usuario administrador '{admin_rut}' ya existe. No se volvió a crear.")
