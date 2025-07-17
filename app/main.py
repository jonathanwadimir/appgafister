from fastapi import FastAPI
from app.database import engine
from app.models.base import Base
from app.routers import (
    tecnico, cliente, ticket, postulacion, evaluacion, usuario
)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Sistema de Tickets Técnicos",
    description="API para gestión de técnicos, clientes y tickets con integración Telegram",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(tecnico.router, prefix="/tecnicos", tags=["Técnicos"])
app.include_router(cliente.router, prefix="/clientes", tags=["Clientes"])
app.include_router(ticket.router, prefix="/tickets", tags=["Tickets"])
app.include_router(postulacion.router, prefix="/postulaciones", tags=["Postulaciones"])
app.include_router(evaluacion.router, prefix="/evaluaciones", tags=["Evaluaciones"])
app.include_router(usuario.router, prefix="/auth", tags=["Autenticación"])

# Crear tablas si no existen
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
