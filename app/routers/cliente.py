from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.cliente import ClienteCreate
from app.database import get_db
from app.crud.cliente import crear_cliente, listar_clientes

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

@router.post("/", response_model=dict)
async def registrar_cliente(cliente: ClienteCreate, db: AsyncSession = Depends(get_db)):
    nuevo = await crear_cliente(db, cliente)
    return {"mensaje": "Cliente creado", "id": nuevo.id}

@router.get("/", response_model=list)
async def obtener_clientes(db: AsyncSession = Depends(get_db)):
    clientes = await listar_clientes(db)
    return clientes
