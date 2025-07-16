from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from app.crud import get_cliente_by_rut, create_cliente, create_ticket
from app.database import async_session
from app.models import Cliente, Ticket
from app.postulaciones import registrar_postulacion, esta_en_postulacion, obtener_postulantes
from app.crud import get_tecnico_by_rut, get_ticket_by_id  # crea estas funciones si no existen
from telegram import ReplyKeyboardRemove
from sqlalchemy.future import select
from app.models import Ticket

import asyncio

# Estados para login
LOGIN_RUT = 20  # el número lo defines para que no choque con otros estados

async def login_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Por favor, ingresa tu RUT para iniciar sesión como técnico (sin puntos ni guiones)."
    )
    return LOGIN_RUT

async def get_tickets_abiertos(db):
    # Asumiendo que hay un campo 'estado' o similar para filtrar tickets abiertos
    # Si no tienes, filtra por lo que definas como abierto
    result = await db.execute(select(Ticket).where(Ticket.estado == "abierto"))
    tickets = result.scalars().all()
    return tickets

async def mostrar_tickets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'tecnico' not in context.user_data:
        await update.message.reply_text("Debes iniciar sesión primero con /login.")
        return

    from app.crud import get_tickets_abiertos

    async with async_session() as db:
        tickets = await get_tickets_abiertos(db)

    if not tickets:
        await update.message.reply_text("No hay tickets disponibles para postulación.")
        return

    mensaje = "Tickets disponibles para postular:\n\n"
    for t in tickets:
        mensaje += f"ID: {t.id} - {t.descripcion[:50]}...\n"

    mensaje += "\nPara postular, escribe: /postular <ID del ticket>"
    await update.message.reply_text(mensaje)

async def login_rut(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rut = update.message.text.strip()

    from app.crud import get_tecnico_by_rut
    async with async_session() as db:
        tecnico = await get_tecnico_by_rut(db, rut)

    if tecnico is None:
        await update.message.reply_text(
            "No encontré ningún técnico con ese RUT. Por favor intenta de nuevo o usa /cancel para salir.",
            reply_markup=ReplyKeyboardRemove()
        )
        return LOGIN_RUT
    else:
        # Guardamos en user_data que el técnico está "loggeado"
        context.user_data['tecnico'] = {
            'rut': tecnico.rut,
            'nombre': tecnico.nombre,
            'id': tecnico.id
        }
        await update.message.reply_text(
            f"¡Bienvenido {tecnico.nombre}! Has iniciado sesión correctamente.",
            reply_markup=ReplyKeyboardRemove()
        )
        # Aquí puedes mandar a un menú o a lo que quieras que haga el técnico tras login
        return ConversationHandler.END

# Estados para conversación
(RUT, NOMBRE, DESCRIPCION, EMERGENCIA, MULTIMEDIA, CONFIRMACION) = range(6)
(TEC_RUT, TEC_ZONA, TEC_NOMBRE, TEC_CERTIFICADO, TEC_EMISION, TEC_FOTO, TEC_AVISO) = range(6, 13)
async def tecnico_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Registro de Técnico - Paso 1\nPor favor, ingresa tu RUT sin puntos ni guiones.")
    return TEC_RUT

async def recibir_tec_rut(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['rut'] = update.message.text.strip()
    await update.message.reply_text("¿Cuál es tu zona de cobertura? (Ej: Metropolitana)")
    return TEC_ZONA

async def recibir_tec_zona(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['zona'] = update.message.text.strip()
    await update.message.reply_text("¿Cuál es tu nombre completo?")
    return TEC_NOMBRE

async def recibir_tec_nombre(update, context):
    context.user_data['nombre'] = update.message.text.strip()
    reply_keyboard = [["1", "2"]]
    await update.message.reply_text(
    "¿Tienes certificación SEC?\n1. Sí\n2. No\n\nPor favor responde con 1 o 2.",
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return TEC_CERTIFICADO

# recibir_tec_certificado modificado:

async def recibir_tec_certificado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta = update.message.text.strip()

    if respuesta not in ["1", "2"]:
        await update.message.reply_text("Respuesta inválida. Escribe 1 para Sí o 2 para No.")
        return TEC_CERTIFICADO

    context.user_data['certificado'] = respuesta == "1"

    reply_keyboard = [["1", "2", "3"]]
    await update.message.reply_text(
        "¿Qué tipo de documento emites?\n"
        "1. Boleta\n"
        "2. Factura\n"
        "3. Boleta/Factura\n"
        "Por favor responde con 1, 2 o 3.",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return TEC_EMISION

# recibir_tec_foto modificado (solo el mensaje y teclado):

async def recibir_tec_emision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta = update.message.text.strip()

    opciones = {
        "1": "Boleta",
        "2": "Factura",
        "3": "Boleta/Factura"
    }

    if respuesta not in opciones:
        await update.message.reply_text("Opción inválida. Por favor responde con 1, 2 o 3.")
        return TEC_EMISION

    context.user_data['emision'] = opciones[respuesta]
    await update.message.reply_text(
        "Envía una foto tuya para tu perfil. Esta imagen será compartida al postular a un ticket."
    )
    return TEC_FOTO

async def recibir_tec_foto(update, context):
    if not update.message.photo:
        await update.message.reply_text("Debes enviar una imagen.")
        return TEC_FOTO
    file_id = update.message.photo[-1].file_id
    context.user_data['foto'] = file_id
    reply_keyboard = [["1", "2"]]
    await update.message.reply_text(
    "Antes de continuar, debes aceptar las condiciones de uso:\n\n"
    "- El sistema es automático y por postulación\n"
    "- El cliente selecciona entre técnicos disponibles en 10 minutos\n"
    "- Si no hay selección, se asigna al primero que postule en ventana de 5 minutos\n"
    "- El sistema funciona con trazabilidad y evaluaciones\n\n"
    "¿Aceptas las condiciones?\n1. Sí\n2. No\nPor favor responde con 1 o 2.",
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return TEC_AVISO

# recibir_tec_aviso modificado:

async def recibir_tec_aviso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta = update.message.text.strip()

    if respuesta not in ["1", "2"]:
        await update.message.reply_text("Respuesta inválida. Escribe 1 para Sí o 2 para No.")
        return TEC_AVISO

    if respuesta == "2":
        await update.message.reply_text("No puedes continuar si no aceptas las condiciones. Registro cancelado.")
        return ConversationHandler.END

    context.user_data['acepto'] = True

    from app.models.tecnico import Tecnico
    from app.crud import create_tecnico

    async with async_session() as db:
        tecnico = Tecnico(
            rut=context.user_data['rut'],
            zona=context.user_data['zona'],
            nombre=context.user_data['nombre'],
            certificado_sec=context.user_data['certificado'],
            emision=context.user_data['emision'],
            foto_perfil=context.user_data['foto'],
            acepto_terminos=True
        )
        await create_tecnico(db, tecnico)

    await update.message.reply_text("✅ Registro completado. Ya puedes iniciar sesión como técnico.")
    return ConversationHandler.END


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Bienvenido a APPGafister! Para crear un ticket, por favor ingresa tu RUT sin puntos ni guiones."
    )
    return RUT

async def recibir_rut(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rut = update.message.text.strip()
    async with async_session() as db:
        cliente = await get_cliente_by_rut(db, rut)
        if cliente:
            context.user_data['cliente'] = cliente
            await update.message.reply_text(f"Hola {cliente.nombre}, ¿puedes describir el problema?")
            return DESCRIPCION
        else:
            context.user_data['rut'] = rut
            await update.message.reply_text("No te encuentro en el sistema. ¿Cuál es tu nombre completo?")
            return NOMBRE

async def recibir_nombre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.message.text.strip()
    rut = context.user_data.get('rut')
    async with async_session() as db:
        nuevo_cliente = Cliente(rut=rut, nombre=nombre)
        cliente = await create_cliente(db, nuevo_cliente)
        context.user_data['cliente'] = cliente
    await update.message.reply_text("Gracias, ahora describe el problema con detalle.")
    return DESCRIPCION

async def recibir_descripcion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    descripcion = update.message.text.strip()
    context.user_data['descripcion'] = descripcion
    reply_keyboard = [["1", "2"]]
    await update.message.reply_text(
    "¿Es una emergencia?\n\n"
    "⚠️ Si es fuera de horario (20:00 a 08:00), se considera emergencia automática y puede tener recargo adicional.\n\n"
    "1. Sí\n"
    "2. No\n"
    "Por favor responde con 1 o 2.",
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
)
    return EMERGENCIA

async def recibir_emergencia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta = update.message.text.strip()

    if respuesta == "1":
        emergencia = True
    elif respuesta == "2":
        emergencia = False
    else:
        await update.message.reply_text("Opción inválida. Por favor responde con 1 o 2.")
        return EMERGENCIA

    context.user_data['emergencia'] = emergencia
    await update.message.reply_text("Por favor, envía imágenes del problema (puedes enviar varias). Cuando termines, escribe /fin.")
    return MULTIMEDIA

async def recibir_multimedia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Guardar imágenes (por simplicidad, solo la primera imagen en este ejemplo)
    if 'imagenes' not in context.user_data:
        context.user_data['imagenes'] = []
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        context.user_data['imagenes'].append(file_id)
        await update.message.reply_text("Imagen recibida. Puedes enviar más o escribir /fin para terminar.")
    else:
        await update.message.reply_text("Por favor envía solo imágenes o /fin para terminar.")
    return MULTIMEDIA

async def fin_multimedia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Guardar ticket en BD
    cliente = context.user_data.get('cliente')
    descripcion = context.user_data.get('descripcion')
    emergencia = context.user_data.get('emergencia')
    imagenes = context.user_data.get('imagenes', [])
    multimedia = ",".join(imagenes)  # Ejemplo simple: almacenar file_ids separados por coma
    async with async_session() as db:
        ticket = Ticket(
            cliente_id=cliente.id,
            descripcion=descripcion,
            emergencia=emergencia,
            multimedia=multimedia,
        )
        await create_ticket(db, ticket)
    await update.message.reply_text(f"Tu ticket ha sido creado y está en pool para postulación. Gracias por usar APPGafister.")
    return ConversationHandler.END

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Has cancelado la creación del ticket.")
    return ConversationHandler.END

async def postular_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'tecnico' not in context.user_data:
        await update.message.reply_text("Debes iniciar sesión primero con /login.")
        return

    if len(context.args) == 0:
        await update.message.reply_text("Debes indicar el ID del ticket. Ejemplo: /postular 3")
        return

    try:
        ticket_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("El ID debe ser un número.")
        return

    from app.crud import get_ticket_by_id, asignar_tecnico_a_ticket

    async with async_session() as db:
        ticket = await get_ticket_by_id(db, ticket_id)
        if not ticket:
            await update.message.reply_text("Ticket no encontrado.")
            return

        if ticket.tecnico_id is not None:
            await update.message.reply_text("Este ticket ya fue asignado a otro técnico.")
            return

        tecnico_id = context.user_data['tecnico']['id']
        await asignar_tecnico_a_ticket(db, ticket, tecnico_id)
        await update.message.reply_text(f"Has postulado exitosamente al ticket ID {ticket_id}.")

async def postular(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Verifica que haya argumento (ID ticket)
    if not context.args or len(context.args) != 1:
        await update.message.reply_text("Debes escribir el ID del ticket, ej: /postular 123")
        return

    ticket_id_str = context.args[0]
    if not ticket_id_str.isdigit():
        await update.message.reply_text("El ID del ticket debe ser un número.")
        return

    ticket_id = int(ticket_id_str)

    rut_tecnico = update.message.from_user.username  # Aquí puedes cambiar según cómo identifiques al técnico
    if not rut_tecnico:
        await update.message.reply_text("No se pudo identificar tu usuario técnico. Asegúrate de tener un username.")
        return

    # Busca técnico en BD
    async with async_session() as db:
        tecnico = await get_tecnico_by_rut(db, rut_tecnico)
        if not tecnico:
            await update.message.reply_text("No estás registrado como técnico.")
            return

        ticket = await get_ticket_by_id(db, ticket_id)
        if not ticket:
            await update.message.reply_text(f"No encontré el ticket con ID {ticket_id}.")
            return

        if not esta_en_postulacion(ticket_id):
            await update.message.reply_text(f"El ticket {ticket_id} ya no está en fase de postulación.")
            return

    # Registra postulación
    registrar_postulacion(ticket_id, rut_tecnico)
    await update.message.reply_text(f"✅ Postulación registrada para el ticket {ticket_id}. ¡Suerte!")

async def mostrar_tickets(update: Update, context: ContextTypes.DEFAULT_TYPE):
   
    # Validar que técnico está logueado
    if 'tecnico' not in context.user_data:
        await update.message.reply_text("Debes iniciar sesión primero con /login.")
        return
    
    from app.crud import get_tickets_abiertos  # función que debes crear para listar tickets abiertos
    
    async with async_session() as db:
        tickets = await get_tickets_abiertos(db)
    
    if not tickets:
        await update.message.reply_text("No hay tickets disponibles para postulación.")
        return
    
    mensaje = "Tickets disponibles:\n"
    for t in tickets:
        mensaje += f"ID: {t.id} - {t.descripcion[:50]}...\n"
    
    await update.message.reply_text(mensaje)

def main():
    app = ApplicationBuilder().token("7698971858:AAEQ4iE1IRB5T6nCBfxDmfHEzi3HIwDjR_s").build()
    LOGIN = LOGIN_RUT
    login_conv = ConversationHandler(
        entry_points=[CommandHandler("login", login_start)],
        states={
            LOGIN_RUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_rut)],
        },
        fallbacks=[CommandHandler("cancel", cancelar)],
    )
    app.add_handler(login_conv)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            RUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_rut)],
            NOMBRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_nombre)],
            DESCRIPCION: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_descripcion)],
            EMERGENCIA: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_emergencia)],
            MULTIMEDIA: [
                MessageHandler(filters.PHOTO, recibir_multimedia),
                CommandHandler('fin', fin_multimedia)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancelar)]
    )
    tec_conv = ConversationHandler(
        entry_points=[CommandHandler("tecnico", tecnico_start)],
        states={
            TEC_RUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_tec_rut)],
            TEC_ZONA: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_tec_zona)],
            TEC_NOMBRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_tec_nombre)],
            TEC_CERTIFICADO: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_tec_certificado)],
            TEC_EMISION: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_tec_emision)],
            TEC_FOTO: [MessageHandler(filters.PHOTO, recibir_tec_foto)],
            TEC_AVISO: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_tec_aviso)],
        },
        fallbacks=[CommandHandler("cancel", cancelar)],
    )
    
    #app.add_handler(CommandHandler("postular", postular))   
    app.add_handler(conv_handler)
    app.add_handler(tec_conv)
    app.add_handler(CommandHandler("tickets", mostrar_tickets))
    app.add_handler(CommandHandler("postular", postular_ticket))
    app.run_polling()

if __name__ == '__main__':
    main()
