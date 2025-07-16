import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.tecnico import Tecnico
from app.models.ticket import Ticket
from app.models.cliente import Cliente
from app import crud

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def run_tests():
    await setup_database()

    async with AsyncSessionLocal() as session:
        # Test Cliente
        cliente = Cliente(nombre="Juan", rut="12345678-9")
        await crud.create_cliente(session, cliente)

        cliente_db = await crud.get_cliente_by_rut(session, rut="12345678-9")
        print("Cliente obtenido:", cliente_db.nombre, cliente_db.rut)

        # Test Técnico
        tecnico = Tecnico(
            nombre="Pedro", rut="99999999-9", zona="Norte", certificado_sec=True,
            emision="2024-01-01", foto_perfil="foto.jpg", acepto_terminos=True
        )
        await crud.create_tecnico(session, tecnico)
        tecnico_db = await crud.get_tecnico(session, rut="99999999-9")
        print("Técnico obtenido:", tecnico_db.nombre, tecnico_db.rut)

        # Test Ticket
        ticket = Ticket(
            descripcion="Caño roto", cliente_id=cliente_db.id,
            emergencia=True, multimedia=None
        )
        await crud.create_ticket(session, ticket)
        tickets = await crud.get_tickets_by_cliente(session, cliente_id=cliente_db.id)
        print("Tickets del cliente:", len(tickets))

        # Asignar técnico
        ticket_db = tickets[0]
        await crud.asignar_tecnico_a_ticket(session, ticket_db, tecnico_id=tecnico_db.id)
        print("Técnico asignado al ticket:", ticket_db.tecnico_id)

        # Evaluar ticket
        await crud.update_ticket(session, ticket_db.id, evaluacion=5, comentario="Excelente", recomendaria=True)
        print("Evaluación del ticket:", ticket_db.evaluacion, ticket_db.comentario, ticket_db.recomendaria)

if __name__ == "__main__":
    asyncio.run(run_tests())
