from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ticket import Ticket
from app.models.tecnico import Tecnico
from app.models.cliente import Cliente
from app.models.postulacion import Postulacion
from app.models.usuario import Usuario
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# === Técnicos ===
async def get_tecnico(db: AsyncSession, rut: str):
    result = await db.execute(select(Tecnico).where(Tecnico.rut == rut))
    return result.scalars().first()

async def get_tecnicos(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Tecnico).offset(skip).limit(limit))
    return result.scalars().all()

async def create_tecnico(db: AsyncSession, tecnico: Tecnico):
    db.add(tecnico)
    await db.commit()
    await db.refresh(tecnico)
    return tecnico

async def update_tecnico(db: AsyncSession, tecnico: Tecnico):
    await db.commit()
    await db.refresh(tecnico)
    return tecnico

async def delete_tecnico(db: AsyncSession, tecnico: Tecnico):
    await db.delete(tecnico)
    await db.commit()

# === Clientes ===
async def get_cliente_by_rut(db: AsyncSession, rut: str):
    result = await db.execute(select(Cliente).where(Cliente.rut == rut))
    return result.scalars().first()

async def create_cliente(db: AsyncSession, cliente: Cliente):
    db.add(cliente)
    await db.commit()
    await db.refresh(cliente)
    return cliente

async def get_clientes(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Cliente).offset(skip).limit(limit))
    return result.scalars().all()

# === Tickets ===
async def create_ticket(db: AsyncSession, ticket: Ticket):
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket

async def get_tickets_by_cliente(db: AsyncSession, cliente_id: int, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Ticket).where(Ticket.cliente_id == cliente_id).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def get_tickets_abiertos(db: AsyncSession):
    result = await db.execute(select(Ticket).where(Ticket.tecnico_id == None))
    return result.scalars().all()

async def get_ticket_by_id(db: AsyncSession, ticket_id: int):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    return result.scalars().first()

async def asignar_tecnico_a_ticket(db: AsyncSession, ticket: Ticket, tecnico_id: int):
    ticket.tecnico_id = tecnico_id
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket

async def update_ticket(db: AsyncSession, ticket_id: int, evaluacion: int, comentario: str | None = None, recomendaria: bool | None = None):
    ticket = await get_ticket_by_id(db, ticket_id)
    if not ticket:
        return None
    ticket.evaluacion = evaluacion
    ticket.comentario_evaluacion = comentario
    if hasattr(ticket, "recomendaria"):
        ticket.recomendaria = recomendaria
    await db.commit()
    await db.refresh(ticket)
    return ticket

# === Postulaciones ===
async def crear_postulacion(db: AsyncSession, ticket_id: int, tecnico_id: int):
    result = await db.execute(
        select(Postulacion).where(
            Postulacion.ticket_id == ticket_id,
            Postulacion.tecnico_id == tecnico_id
        )
    )
    existente = result.scalar_one_or_none()
    if existente:
        return None

    nueva = Postulacion(ticket_id=ticket_id, tecnico_id=tecnico_id)
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva

async def get_postulaciones_por_ticket(db: AsyncSession, ticket_id: int):
    result = await db.execute(
        select(Postulacion).where(Postulacion.ticket_id == ticket_id)
    )
    return result.scalars().all()

async def get_postulaciones_por_tecnico(db: AsyncSession, tecnico_id: int):
    result = await db.execute(
        select(Postulacion).where(Postulacion.tecnico_id == tecnico_id)
    )
    return result.scalars().all()

async def actualizar_estado_asignacion(db: AsyncSession, ticket_id: int, nuevo_estado: str):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    if ticket:
        ticket.estado_asignacion = nuevo_estado
        await db.commit()
        await db.refresh(ticket)
        return ticket
    return None

async def get_tickets(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Ticket).offset(skip).limit(limit))
    return result.scalars().all()

# === Nueva función: Asignar siguiente técnico postulado ===
async def asignar_siguiente_tecnico(db: AsyncSession, ticket_id: int):
    ticket = await get_ticket_by_id(db, ticket_id)
    if not ticket:
        return None

    result = await db.execute(
        select(Postulacion).where(Postulacion.ticket_id == ticket_id)
    )
    postulaciones = result.scalars().all()

    for postulacion in postulaciones:
        if ticket.tecnico_id != postulacion.tecnico_id:
            ticket.tecnico_id = postulacion.tecnico_id
            ticket.estado_asignacion = "pendiente"
            await db.commit()
            await db.refresh(ticket)
            return ticket

    ticket.tecnico_id = None
    ticket.estado_asignacion = "sin_postulantes"
    await db.commit()
    await db.refresh(ticket)
    return ticket

# === Usuarios (Autenticación) ===
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(Usuario).where(Usuario.username == username))
    return result.scalars().first()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def create_user(db: AsyncSession, username: str, password: str, rol: str = "cliente"):
    hashed_password = get_password_hash(password)
    new_user = Usuario(username=username, hashed_password=hashed_password, rol=rol)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user