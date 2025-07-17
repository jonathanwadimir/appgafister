# app/telegram/bot.py

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

TELEGRAM_TOKEN = "7698971858:AAEQ4iE1IRB5T6nCBfxDmfHEzi3HIwDjR_s"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

class LoginStates(StatesGroup):
    waiting_for_rut = State()
    waiting_for_password = State()

fake_user_db = {
    "12345678-9": {"password": "pass123", "role": "tecnico", "name": "Juan Pérez"},
    "98765432-1": {"password": "pass456", "role": "cliente", "name": "Maria Lopez"},
    "11111111-1": {"password": "adminpass", "role": "admin", "name": "Admin"},
}

user_sessions = {}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = (
        "👋 <b>Bienvenido al Sistema de Gestión de Tickets para Servicio Técnico</b>\n\n"
        "👤 <b>Clientes:</b>\n"
        "  • /crear_ticket - Crear un ticket\n"
        "  • /seleccionar_tecnico - Elegir técnico de postulantes\n"
        "  • /evaluar_tecnico - Evaluar técnico\n\n"
        "🛠️ Si eres técnico, haz /login con tus credenciales para entrar al portal.\n\n"
        "ℹ️ Usa /help para más información."
    )
    await message.answer(text, parse_mode="HTML")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    text = (
        "❓ <b>Ayuda y comandos disponibles:</b>\n\n"
        "Para todos los usuarios:\n"
        "/start - Mostrar menú principal\n"
        "/login - Iniciar sesión (técnicos/admins)\n"
        "/crear_ticket - Crear ticket (clientes)\n"
        "/pool - Tickets disponibles (técnicos)\n"
        "/mis_asignados - Tus tickets asignados (técnicos)\n\n"
        "Otros comandos requieren sesión activa según tu rol."
    )
    await message.answer(text, parse_mode="HTML")

async def enviar_menu_rol(chat_id: int, role: str):
    if role == "cliente":
        texto = (
            "👤 <b>Opciones para Clientes:</b>\n"
            "• /crear_ticket - Crear un ticket\n"
            "• /seleccionar_tecnico - Elegir técnico de postulantes\n"
            "• /evaluar_tecnico - Evaluar técnico\n"
        )
    elif role == "tecnico":
        texto = (
            "🛠️ <b>Opciones para Técnicos:</b>\n"
            "• /pool - Ver tickets disponibles\n"
            "• /mis_asignados - Ver tickets asignados\n"
            "• /iniciar_trabajo - Marcar inicio del trabajo\n"
            "• /cerrar_trabajo - Cerrar ticket con resumen y cobro\n"
            "• /enviar_comprobante - Enviar comprobante de recargos\n"
        )
    elif role == "admin":
        texto = (
            "👮 <b>Opciones para Administradores:</b>\n"
            "• /validar_pago - Validar comprobantes\n"
            "• /reporte_deudas - Ver reportes de deudas\n"
        )
    else:
        texto = "Rol desconocido."
    texto += "\nℹ️ Usa /help para más información."
    await bot.send_message(chat_id, texto, parse_mode="HTML")

@dp.message(Command("login"))
async def cmd_login_start(message: types.Message, state: FSMContext):
    await message.answer("Por favor, ingresa tu RUT sin puntos ni guiones:")
    await state.set_state(LoginStates.waiting_for_rut)

@dp.message(LoginStates.waiting_for_rut)
async def process_rut(message: types.Message, state: FSMContext):
    rut = message.text.strip()
    await state.update_data(rut=rut)
    await message.answer("Ahora ingresa tu contraseña:")
    await state.set_state(LoginStates.waiting_for_password)

@dp.message(LoginStates.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    password = message.text.strip()
    data = await state.get_data()
    rut = data.get("rut")
    user = fake_user_db.get(rut)
    if user and user["password"] == password:
        user_sessions[message.chat.id] = {
            "rut": rut,
            "role": user["role"],
            "name": user["name"],
        }
        await message.answer(
            f"✅ ¡Bienvenido {user['name']}!\n"
            f"Tu rol es: {user['role']}\n"
            "A continuación, te muestro las opciones disponibles:"
        )
        await enviar_menu_rol(message.chat.id, user["role"])
        await state.clear()
    else:
        await message.answer("❌ RUT o contraseña incorrectos. Intenta de nuevo con /login.")
        await state.clear()

@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    session = user_sessions.get(message.chat.id)
    if not session:
        await message.answer("⚠️ Debes iniciar sesión con /login para ver el menú.")
        return
    await enviar_menu_rol(message.chat.id, session["role"])

# Ejemplo comandos técnicos con validación de sesión y rol
@dp.message(Command("pool"))
async def cmd_pool(message: types.Message):
    session = user_sessions.get(message.chat.id)
    if not session or session["role"] != "tecnico":
        await message.answer("⚠️ Debes iniciar sesión como técnico con /login.")
        return
    await message.answer("📋 Tickets disponibles:\n1. Reparar filtración\n2. Cambio de válvula\n... (simulado)")

@dp.message(Command("mis_asignados"))
async def cmd_mis_asignados(message: types.Message):
    session = user_sessions.get(message.chat.id)
    if not session or session["role"] != "tecnico":
        await message.answer("⚠️ Debes iniciar sesión como técnico con /login.")
        return
    await message.answer("🛠️ Tus tickets asignados:\n#123 - Reparar cañería cocina\n#124 - Revisar calentador")

@dp.message(Command("crear_ticket"))
async def cmd_crear_ticket(message: types.Message):
    session = user_sessions.get(message.chat.id)
    if not session or session["role"] != "cliente":
        await message.answer("⚠️ Solo clientes pueden crear tickets. Por favor, inicia sesión o regístrate.")
        return
    await message.answer("Por favor, describe el problema y adjunta fotos o videos (opcional).")

async def main():
    print("Bot iniciado...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
