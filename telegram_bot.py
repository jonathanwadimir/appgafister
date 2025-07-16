import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

API_URL = "http://127.0.0.1:8000"  # Cambia según tu backend
BOT_TOKEN = "7698971858:AAEQ4iE1IRB5T6nCBfxDmfHEzi3HIwDjR_s"  # Pon aquí tu token real

# En producción, el token debe estar en variables de entorno o config segura

# Para simplificar, vamos a usar un token estático para el técnico en este ejemplo
TECNICO_TOKEN = "token_del_tecnico_para_llamar_api"  # Se puede mejorar autenticación en bot

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola! Soy tu bot de soporte técnico. Usa /tickets para ver tickets abiertos."
    )

async def tickets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    headers = {"Authorization": f"Bearer {TECNICO_TOKEN}"}
    response = requests.get(f"{API_URL}/tickets?skip=0&limit=10", headers=headers)
    if response.status_code == 200:
        tickets = response.json()
        if tickets:
            mensajes = []
            for t in tickets:
                mensajes.append(f"Ticket #{t['id']}: {t['descripcion']}\nEstado: {t['estado_asignacion']}")
            await update.message.reply_text("\n\n".join(mensajes))
        else:
            await update.message.reply_text("No hay tickets abiertos.")
    else:
        await update.message.reply_text("Error al obtener tickets.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tickets", tickets))

    print("Bot iniciado...")
    app.run_polling()
