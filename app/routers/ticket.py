from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.ticket import Ticket
from app.models.usuario import Usuario
from app.schemas import TicketCreate, TicketOut, TicketEvaluacion, TicketAsignacionUpdate, TicketOut as TicketRead
from app.crud import (
    create_ticket,
    get_tickets_by_cliente,
    get_ticket_by_id,
    actualizar_estado_asignacion,
    get_tickets,
    asignar_siguiente_tecnico,  # ✅ necesario para reasignación automática
)
from typing import List
from app.auth.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=TicketOut)
async def crear_ticket(
    ticket: TicketCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return await create_ticket(db, Ticket(**ticket.dict()))

@router.get("/cliente/{rut}", response_model=List[TicketOut])
async def listar_tickets_cliente(
    rut: str,
    db: AsyncSession = Depends(get_db)
):
    from app.crud import get_cliente_by_rut
    cliente = await get_cliente_by_rut(db, rut)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return await get_tickets_by_cliente(db, cliente.id)

@router.get("/", response_model=List[TicketOut])
async def listar_tickets(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await get_tickets(db, skip=skip, limit=limit)

@router.put("/evaluar", response_model=TicketOut)
async def evaluar_ticket(
    evaluacion: TicketEvaluacion,
    db: AsyncSession = Depends(get_db)
):
    ticket = await get_ticket_by_id(db, evaluacion.ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    
    ticket.evaluacion = evaluacion.evaluacion
    ticket.comentario_evaluacion = evaluacion.comentario
    await db.commit()
    await db.refresh(ticket)
    return ticket

@router.put("/{ticket_id}/asignacion", response_model=TicketRead)
async def actualizar_estado_ticket(
    ticket_id: int,
    estado_update: TicketAsignacionUpdate,
    db: AsyncSession = Depends(get_db)
):
    ticket = await get_ticket_by_id(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    ticket.estado_asignacion = estado_update.estado_asignacion
    await db.commit()
    await db.refresh(ticket)

    if estado_update.estado_asignacion.lower() == "rechazado":
        ticket = await asignar_siguiente_tecnico(db, ticket_id)

    return ticket
