from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.evaluacion import EvaluacionCreate, EvaluacionOut
from app.crud.evaluacion import crear_evaluacion
from app.auth.auth import require_role
from app.models.usuario import Usuario

router = APIRouter(
    prefix="/evaluaciones",
    tags=["Evaluaciones"]
)

@router.post("/", response_model=EvaluacionOut, status_code=status.HTTP_201_CREATED)
async def registrar_evaluacion(
    datos: EvaluacionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_role("cliente"))
):
    evaluacion = await crear_evaluacion(db, datos)
    if not evaluacion:
        raise HTTPException(status_code=404, detail="Error al crear la evaluación")
    return evaluacion
