from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.ticket import Ticket
from app.models.usuario import Usuario
from app.schemas import TicketCreate, TicketOut, TicketAsignacionUpdate, TicketOut as TicketRead
from app.crud.ticket import (  # <-- Cambiado para importar desde el módulo ticket
    crear_ticket,
    listar_tickets,
    actualizar_estado_asignacion,
)
from typing import List
from app.auth.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=TicketOut)
async def crear_ticket_endpoint(
    ticket: TicketCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return await crear_ticket(db, ticket)

@router.get("/", response_model=List[TicketOut])
async def listar_tickets_endpoint(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    tickets = await listar_tickets(db)
    return tickets

@router.put("/{ticket_id}/asignacion", response_model=TicketRead)
async def actualizar_estado_ticket(
    ticket_id: int,
    estado_update: TicketAsignacionUpdate,
    db: AsyncSession = Depends(get_db)
):
    ticket = await actualizar_estado_asignacion(db, ticket_id, estado_update.estado_asignacion)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket
