import os
import httpx

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
        ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, filters
                          )

# Cargar las variables de entorno de .env
load_dotenv()

# Cargar token de Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Estados para cada flujo de onversaciones
STATE_SMS = 1

# Funcione de los manejadores

"""
    Comando /hello:
    Es un comando de ejemplo para comprobar que el bot está activo
"""
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


"""
    Comando /Start
    Da la bienvenida a un nuevo usuario y muestra el listado de comandos así como las 
    reglas para usar el bot
"""
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Bienvenido {update.effective_user.first_name}!")
    await update.message.reply_text(f"*** REGLAS DEL BOT ***")   


"""
    Comando /help
    Devuelve las reglas y los comandos para interactuar con el bot
"""
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"*** REGLAS DEL BOT ***")   

"""
    No es un comando.
    Este handler trata todos los mensajes con no son capturados por el resto de handlers.
    Avisa al usuario de que no le a entendido, le avisa de que debe usar comandos y que 
    dispone del comando /help para ver todos los comandos
"""
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Lo siento, no entiendo lo que me quieres decir. Recuerda que puedes consular la lista de comandos escribiendo /help.")


"""
    Comando /sms:
    Sirve de punto de entreada (entrypoint) pada la conversación.
    Avisa al bot que va a recibir un mensaje de texto SMS. El bot contesta con un mensaje 
    que reconoce la acción e incluye una breve advertencia.
"""
async def start_sms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Entendido! Estoy listo para analizar el SMS sospechoso.")
    return STATE_SMS

"""
    No es un comando:
    En esta función se ejecuta la lógica para la conversación de procesar un mensaje de texto
    de SMS. Se obtiene el mensaje sospechoso, se envía a la API y se produce un breve reporte
    con algunas indicaciones breves.
"""
async def process_sms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Recibido, me pondré con ello ahora mismo.")
    msg = update.message.text

    # Petición a la API
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/analyse/text/advanced",
            json={"msg": msg}
        )

    status_code = response.status_code
    result = response.json()

    await update.message.reply_text(f"Esto es lo que sabemos: {result}")
    
    return ConversationHandler.END
    


"""
    Comando /cancelar:
    Pone fin a la conversación que está en curso. Esta función es compartida entre todos
    los flujos de conversaciones
"""
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await (update.message.reply_text("Conversación terminada. ¿En qué puedo ayudarte?"))
    return ConversationHandler.END


# Aplicacion
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Manejadores de conversaciones
sms_text_handler = ConversationHandler(
    entry_points=[CommandHandler("sms", start_sms)],
    states={STATE_SMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_sms)]},
    fallbacks=[CommandHandler("cancelar", cancel)]
        )

# Definir los manejadores de comandos
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", info))
app.add_handler(CommandHandler("hello", hello))
app.add_handler(sms_text_handler)
app.add_handler(MessageHandler(filters.ALL, unknown))   # Es el handler por defecto, debe ser el último

# Comienza el bucle de eventos
app.run_polling()

