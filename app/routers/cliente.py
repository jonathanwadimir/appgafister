from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.crud.cliente import get_cliente_by_rut, create_cliente, get_clientes
from app.schemas import ClienteCreate, ClienteOut

router = APIRouter()

@router.post("/", response_model=ClienteOut, tags=["Clientes"])
async def crear_cliente(cliente: ClienteCreate, db: AsyncSession = Depends(get_db)):
    db_cliente = await get_cliente_by_rut(db, cliente.rut)
    if db_cliente:
        raise HTTPException(status_code=400, detail="Cliente ya registrado")
    return await create_cliente(db, cliente)

@router.get("/", response_model=List[ClienteOut], tags=["Clientes"])
async def listar_clientes(db: AsyncSession = Depends(get_db)):
    return await get_clientes(db)
