from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.database import get_db
from app import crud, models
from pydantic import BaseModel

router = APIRouter()

class TecnicoCreate(BaseModel):
    rut: str
    nombre: str
    zona_cobertura: Optional[str] = None
    certificado_sec: Optional[bool] = False
    emision_sii: Optional[str] = None
    foto_perfil_url: Optional[str] = None

@router.post("/")
async def crear_tecnico(tecnico: TecnicoCreate, db: AsyncSession = Depends(get_db)):
    db_tecnico = await crud.get_tecnico(db, tecnico.rut)
    if db_tecnico:
        raise HTTPException(status_code=400, detail="El técnico ya existe")
    nuevo_tecnico = models.Tecnico(
        rut=tecnico.rut,
        nombre=tecnico.nombre,
        zona=tecnico.zona_cobertura,
        certificado_sec=tecnico.certificado_sec,
        emision=tecnico.emision_sii,
        foto_perfil=tecnico.foto_perfil_url,
        acepto_terminos=True
    )
    return await crud.create_tecnico(db, nuevo_tecnico)

@router.get("/")
async def listar_tecnicos(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_tecnicos(db, skip, limit)
