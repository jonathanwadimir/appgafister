from fastapi import FastAPI
from app.database import engine
from app.models.base import Base
from app.utils.crear_admin import crear_usuario_admin

from app.routers import tecnicos, cliente, ticket, auth, usuarios, postulacion, evaluacion_router

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await crear_usuario_admin()

# Routers
app.include_router(tecnicos, prefix="/tecnicos", tags=["Técnicos"])
app.include_router(cliente, prefix="/clientes", tags=["Clientes"])
app.include_router(ticket, prefix="/tickets", tags=["Tickets"])
app.include_router(auth, prefix="/auth", tags=["Autenticación"])  # ✅ Usamos el alias correcto
app.include_router(postulacion, prefix="/postulaciones", tags=["Postulaciones"])
app.include_router(evaluacion_router, prefix="/evaluaciones", tags=["Evaluaciones"])
app.include_router(usuarios)

@app.get("/")
async def root():
    return {"message": "Bienvenido a APPGafister backend"}
