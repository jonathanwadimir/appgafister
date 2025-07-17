from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.auth.auth import get_current_user, require_role
from app.models.usuario import Usuario
from app.schemas.postulacion import PostulacionCreate, PostulacionOut
from app.crud.postulacion import crear_postulacion, obtener_postulaciones_por_ticket, actualizar_estado_postulacion

router = APIRouter(
    prefix="/postulaciones",
    tags=["Postulaciones"]
)

@router.post("/", response_model=PostulacionOut)
async def postular_a_ticket(
    postulacion: PostulacionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_role("tecnico"))
):
    try:
        return await crear_postulacion(db, postulacion)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/ticket/{ticket_id}", response_model=List[PostulacionOut])
async def listar_postulaciones_de_ticket(
    ticket_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    postulaciones = await obtener_postulaciones_por_ticket(db, ticket_id)
    if not postulaciones:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay postulaciones para este ticket")
    return postulaciones

@router.put("/{postulacion_id}/estado", response_model=PostulacionOut)
async def cambiar_estado_postulacion(
    postulacion_id: int,
    nuevo_estado: str,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_role("tecnico"))
):
    try:
        postulacion = await actualizar_estado_postulacion(db, postulacion_id, nuevo_estado)
        if postulacion is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Postulación no encontrada")
        return postulacion
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
