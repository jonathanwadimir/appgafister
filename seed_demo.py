import asyncio
import random
from datetime import datetime, timedelta

from app.database import AsyncSessionLocal, engine
from app.models.base import Base
from app.models.tecnico import Tecnico
from app.models.cliente import Cliente
from app.models.ticket import Ticket
from app.models.evaluacion import Evaluacion

async def seed_demo():
    # Crear las tablas si no existen
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # Limpiar tablas (opcional)
        await session.execute("DELETE FROM evaluaciones")
        await session.execute("DELETE FROM tickets")
        await session.execute("DELETE FROM tecnicos")
        await session.execute("DELETE FROM clientes")
        await session.commit()

        # Insertar Técnicos
        tecnicos = []
        for i in range(5):
            t = Tecnico(
                nombre=f"Técnico {i+1}",
                zona=random.choice(["Norte", "Sur", "Centro"]),
                certificado_sec=bool(random.getrandbits(1)),
                emision=datetime.now() - timedelta(days=random.randint(0, 365)),
            )
            tecnicos.append(t)
            session.add(t)
        await session.commit()

        # Insertar Clientes
        clientes = []
        for i in range(5):
            c = Cliente(
                nombre=f"Cliente {i+1}",
                rut=f"1234567{i}8-{random.randint(0,9)}",
                telefono=f"9{random.randint(10000000, 99999999)}"
            )
            clientes.append(c)
            session.add(c)
        await session.commit()

        # Insertar Tickets
        tickets = []
        for i in range(10):
            ticket = Ticket(
                descripcion=f"Problema técnico #{i+1}",
                cliente_id=random.choice(clientes).id,
                tecnico_id=random.choice(tecnicos).id,
                estado_asignacion=random.choice(["pendiente", "aceptado", "rechazado"])
            )
            tickets.append(ticket)
            session.add(ticket)
        await session.commit()

        # Insertar Evaluaciones para algunos tickets
        for i in range(5):
            evaluacion = Evaluacion(
                ticket_id=random.choice(tickets).id,
                puntuacion=random.randint(1,5),
                comentario="Evaluación demo"
            )
            session.add(evaluacion)
        await session.commit()

    print("✅ Datos de prueba insertados correctamente.")

if __name__ == "__main__":
    asyncio.run(seed_demo())
