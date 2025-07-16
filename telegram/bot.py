import logging
import requests
from telegram import Update, ForceReply
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
)

BOT_TOKEN = "7698971858:AAEQ4iE1IRB5T6nCBfxDmfHEzi3HIwDjR_s"
API_URL = "http://127.0.0.1:8000"

# Estados para ConversationHandler
LOGIN_USER, LOGIN_PASS = range(2)
CREAR_DESC = range(1)

# Almacenamos sesión por chat_id: {"token": ..., "usuario": {...}}
sessions = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# --------- Helpers ---------

def get_headers(chat_id):
    token = sessions.get(chat_id, {}).get("token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy el bot de APPGafister 🚿🔧\n"
        "Usa /login para iniciar sesión.\n"
        "Usa /listartecnicos para ver técnicos.\n"
        "Usa /crearticket para crear un ticket.\n"
        "Usa /mimistickets para ver tus tickets.\n"
        "Usa /postular <ticket_id> para postular a un ticket.\n"
        "Usa /evaluar <ticket_id> <puntuacion> [comentario] para evaluar un ticket."
    )

# --------- Login Flow ---------

async def login_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Por favor envía tu nombre de usuario:")
    return LOGIN_USER

async def login_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['username'] = update.message.text.strip()
    await update.message.reply_text("Ahora envía tu contraseña:")
    return LOGIN_PASS

async def login_pass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.text.strip()
    username = context.user_data.get('username')
    data = {"username": username, "password": password}
    try:
        r = requests.post(f"{API_URL}/auth/login", data=data)
        if r.status_code == 200:
            token = r.json().get("access_token")
            if token:
                user_r = requests.get(f"{API_URL}/auth/users/me", headers={"Authorization": f"Bearer {token}"})
                if user_r.status_code == 200:
                    sessions[update.effective_chat.id] = {
                        "token": token,
                        "usuario": user_r.json()
                    }
                    await update.message.reply_text(f"✅ Login exitoso. Bienvenido {username}!")
                    return ConversationHandler.END
                else:
                    await update.message.reply_text("Error al obtener datos del usuario.")
                    return ConversationHandler.END
            else:
                await update.message.reply_text("Token no recibido. Intenta nuevamente.")
                return ConversationHandler.END
        else:
            await update.message.reply_text("Usuario o contraseña incorrectos. Usa /login para intentar de nuevo.")
            return ConversationHandler.END
    except Exception as e:
        await update.message.reply_text(f"Error de conexión: {e}")
        return ConversationHandler.END

async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in sessions:
        del sessions[chat_id]
        await update.message.reply_text("Has cerrado sesión exitosamente.")
    else:
        await update.message.reply_text("No estás logueado.")
        
# --------- Listar Técnicos ---------

async def listartecnicos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get(f"{API_URL}/tecnicos/")
        if r.status_code == 200:
            tecnicos = r.json()
            if not tecnicos:
                await update.message.reply_text("No hay técnicos registrados.")
                return
            msg = "👷 Técnicos disponibles:\n"
            for t in tecnicos:
                msg += f"- ID {t['id']}: {t['nombre']} (Zona: {t.get('zona','-')}, Certificado: {t.get('certificado_sec','-')})\n"
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text("Error al obtener técnicos.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# --------- Crear Ticket (simple flujo) ---------

async def crearticket_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in sessions:
        await update.message.reply_text("Debes iniciar sesión con /login para crear tickets.")
        return ConversationHandler.END

    await update.message.reply_text("Envía la descripción del problema para el ticket:")
    return CREAR_DESC

async def crearticket_desc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    desc = update.message.text.strip()
    chat_id = update.effective_chat.id
    token = sessions.get(chat_id, {}).get("token")
    user = sessions.get(chat_id, {}).get("usuario")
    if not token or not user:
        await update.message.reply_text("Sesión inválida, por favor inicia sesión de nuevo con /login.")
        return ConversationHandler.END

    # Suponemos que cliente_id viene del usuario (el id o rut, aquí simplifico con id)
    cliente_id = user.get("id")

    data = {"cliente_id": cliente_id, "descripcion": desc}
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = requests.post(f"{API_URL}/tickets/", json=data, headers=headers)
        if r.status_code in [200, 201]:
            await update.message.reply_text("✅ Ticket creado correctamente.")
        else:
            await update.message.reply_text(f"Error al crear ticket: {r.text}")
    except Exception as e:
        await update.message.reply_text(f"Error de conexión: {e}")

    return ConversationHandler.END

# --------- Ver Mis Tickets ---------

async def mimistickets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in sessions:
        await update.message.reply_text("Debes iniciar sesión con /login para ver tus tickets.")
        return
    token = sessions[chat_id]["token"]
    user = sessions[chat_id]["usuario"]
    cliente_id = user.get("id")
    try:
        r = requests.get(f"{API_URL}/tickets/cliente/{cliente_id}", headers={"Authorization": f"Bearer {token}"})
        if r.status_code == 200:
            tickets = r.json()
            if not tickets:
                await update.message.reply_text("No tienes tickets registrados.")
                return
            msg = "🎫 Tus tickets:\n"
            for t in tickets:
                msg += f"- ID {t['id']} - Estado: {t['estado_asignacion']} - Descripción: {t['descripcion']}\n"
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text("Error al obtener tus tickets.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# --------- Postular a Ticket ---------

async def postular(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in sessions:
        await update.message.reply_text("Debes iniciar sesión con /login para postular a un ticket.")
        return
    token = sessions[chat_id]["token"]
    user = sessions[chat_id]["usuario"]

    if len(context.args) < 1:
        await update.message.reply_text("Usa: /postular <ticket_id>")
        return

    ticket_id = context.args[0]
    tecnico_id = user.get("id")

    data = {"tecnico_id": tecnico_id, "ticket_id": int(ticket_id)}
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = requests.post(f"{API_URL}/postulaciones/", json=data, headers=headers)
        if r.status_code in [200, 201]:
            await update.message.reply_text(f"✅ Postulación al ticket {ticket_id} enviada.")
        else:
            await update.message.reply_text(f"Error al postular: {r.text}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# --------- Evaluar Ticket ---------

async def evaluar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in sessions:
        await update.message.reply_text("Debes iniciar sesión con /login para evaluar tickets.")
        return
    token = sessions[chat_id]["token"]

    if len(context.args) < 2:
        await update.message.reply_text("Usa: /evaluar <ticket_id> <puntuacion(1-5)> [comentario]")
        return

    ticket_id = context.args[0]
    try:
        puntuacion = int(context.args[1])
        if puntuacion < 1 or puntuacion > 5:
            raise ValueError
    except ValueError:
        await update.message.reply_text("La puntuación debe ser un número entre 1 y 5.")
        return

    comentario = " ".join(context.args[2:]) if len(context.args) > 2 else ""

    data = {"ticket_id": int(ticket_id), "puntuacion": puntuacion, "comentario": comentario}
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = requests.post(f"{API_URL}/evaluaciones/", json=data, headers=headers)
        if r.status_code in [200, 201]:
            await update.message.reply_text("✅ Evaluación enviada correctamente.")
        else:
            await update.message.reply_text(f"Error al enviar evaluación: {r.text}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# --------- Cancelar conversaciones ---------

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operación cancelada.")
    return ConversationHandler.END

# --------- Main ---------

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Conversación para login
    login_conv = ConversationHandler(
        entry_points=[CommandHandler("login", login_start)],
        states={
            LOGIN_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_user)],
            LOGIN_PASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_pass)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Conversación para crear ticket
    crear_ticket_conv = ConversationHandler(
        entry_points=[CommandHandler("crearticket", crearticket_start)],
        states={
            CREAR_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, crearticket_desc)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(login_conv)
    app.add_handler(CommandHandler("logout", logout))
    app.add_handler(CommandHandler("listartecnicos", listartecnicos))
    app.add_handler(crear_ticket_conv)
    app.add_handler(CommandHandler("mimistickets", mimistickets))
    app.add_handler(CommandHandler("postular", postular))
    app.add_handler(CommandHandler("evaluar", evaluar))
    app.add_handler(CommandHandler("cancel", cancel))

    print("✅ Bot corriendo... Esperando mensajes en Telegram")
    app.run_polling()

if __name__ == "__main__":
    main()
