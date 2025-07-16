from datetime import datetime, timedelta

# Estructura en memoria (puede reemplazarse por base de datos si necesitas persistencia)
postulaciones_tickets = {}  # {ticket_id: {"tecnicos": [rut1, rut2], "expira": datetime}}

# Función para registrar una postulación
def registrar_postulacion(ticket_id: int, rut_tecnico: str):
    ahora = datetime.now()
    if ticket_id not in postulaciones_tickets:
        postulaciones_tickets[ticket_id] = {
            "tecnicos": [rut_tecnico],
            "expira": ahora + timedelta(minutes=10)  # tiempo para que cliente elija
        }
    else:
        if rut_tecnico not in postulaciones_tickets[ticket_id]["tecnicos"]:
            postulaciones_tickets[ticket_id]["tecnicos"].append(rut_tecnico)

# Función para obtener técnicos postulados a un ticket
def obtener_postulantes(ticket_id: int):
    return postulaciones_tickets.get(ticket_id, {}).get("tecnicos", [])

# Función para verificar si un ticket aún está en fase de postulación
def esta_en_postulacion(ticket_id: int):
    data = postulaciones_tickets.get(ticket_id)
    if data:
        return datetime.now() < data["expira"]
    return False
