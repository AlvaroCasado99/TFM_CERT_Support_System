import os
import httpx

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
        ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, filters
                          )

from responses import responses

# Cargar las variables de entorno de .env
load_dotenv()

# Cargar token de Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Estados para cada flujo de onversaciones
STATE_SMS = 1

# Variables globales
DEFAULT_LENG = "es"

# Funcione de los manejadores

"""
    Comando /hello:
    Es un comando de ejemplo para comprobar que el bot está activo
"""
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    greetings = responses[DEFAULT_LENG]['greetings']
    await update.message.reply_text(f'{greetings} {update.effective_user.first_name}')


"""
    Comando /Start
    Da la bienvenida a un nuevo usuario y muestra el listado de comandos así como las 
    reglas para usar el bot
"""
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    greetings = responses[DEFAULT_LENG]['greetings']
    rules = responses[DEFAULT_LENG]['rules']
    commands = responses[DEFAULT_LENG]['commands']
    disclaimer = responses[DEFAULT_LENG]['ia_act']
    await update.message.reply_text(f'{greetings} {update.effective_user.first_name}')
    await update.message.reply_text(rules)   
    await update.message.reply_text(commands)   
    await update.message.reply_text(disclaimer)   


"""
    Comando /help
    Devuelve las reglas y los comandos para interactuar con el bot
"""
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    rules = responses[DEFAULT_LENG]['rules']
    commands = responses[DEFAULT_LENG]['commands']
    await update.message.reply_text(rules)   
    await update.message.reply_text(commands)   


"""
    Comando /commands
    Devuelve los comandos para interactuar con el bot
"""
async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    commands = responses[DEFAULT_LENG]['commands']
    await update.message.reply_text(commands)


"""
    Comando /privacy
    Devuelve la política de privacidad de esta aplicación
"""
async def privacy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    legal_priv = responses[DEFAULT_LENG]['privacy']
    await update.message.reply_text(legal_priv)



"""
    No es un comando.
    Este handler trata todos los mensajes con no son capturados por el resto de handlers.
    Avisa al usuario de que no le a entendido, le avisa de que debe usar comandos y que 
    dispone del comando /help para ver todos los comandos
"""
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(responses[DEFAULT_LENG]["unknown"])


"""
    Comando /sms:
    Sirve de punto de entreada (entrypoint) pada la conversación.
    Avisa al bot que va a recibir un mensaje de texto SMS. El bot contesta con un mensaje 
    que reconoce la acción e incluye una breve advertencia.
"""
async def start_sms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(responses[DEFAULT_LENG]["smsh_ready"])
    return STATE_SMS


"""
    Genera una respuesta en función del resultado de un mensaje.
"""
def _generate_response(data, lang: str ="es"):
    response = ""

    if data["flavour"] == "ham":
        response = responses[lang]["smsh_safe"]
    
    else:
        # Construir la respuesta con los datos
        response = "\n" + responses[lang]["smsh_flavour"].replace("$$FLAVOUR$$", data["flavour"]) + "\n"
        if isinstance(data['entity'], str):
            response += "\n" +  responses[lang]["smsh_entity"].replace("$$ENTITY$$", data["entity"]) + "\n"
        else:
            response += "\n" + responses[lang]["smsh_entities"].replace("$$ENTITIES$$", ", ".join(data["entity"])) + "\n"

        if data['url']:
            response += "\n" + responses[lang]["smsh_url"] + "\n"
    
        response = responses[lang]["smsh_result"] + "\n" + response

    return response

"""
    Hace la peticion a la api para analizar un mensaje
"""
async def _analyse_message(msg: str):
    try:
        # Lanzar peticion a la API
        async with httpx.AsyncClient() as client:
            res = await client.post(
                "http://localhost:8000/analyse/text/advanced",
                json={"msg": msg}
            )
        
        res.raise_for_status()
        return {"ok": True,  "data": res.json()}
    
    except httpx.RequestError as e:
        print(f"Request Error {e}")
        return {"ok": False, "error": "Error de conexión. Inténtelo más tarde."}

    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code
        print(f"He recogido este error: {status_code} -> {e}")
        if status_code >= 500:
            return {"ok": False, "error": "Error del servidor. Inténtelo más tarde."}
        else:
            return {"ok": False, "error": f"Ha ocurrido un error inesperado ({status_code})."}
    except Exception as e:
        return {"ok": False, "error": f"Ha ocurrido un error inesperado ({e})."}


"""
    No es un comando:
    En esta función se ejecuta la lógica para la conversación de procesar un mensaje de texto
    de SMS. Se obtiene el mensaje sospechoso, se envía a la API y se produce un breve reporte
    con algunas indicaciones breves.
"""
async def process_sms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(responses[DEFAULT_LENG]["smsh_go"])
    msg = update.message.text
    response = ""

    # Petición a la API
    result = await _analyse_message(msg)

    # Contruir la respuesta
    if result['ok']:
        response = _generate_response(result['data'], lang=DEFAULT_LENG)
    else:
        print(result['error'])
        response = responses[DEFAULT_LENG]['smsh_error']

    # Mostrar la respuesta
    await update.message.reply_text(response)
    
    return ConversationHandler.END
    


"""
    Comando /cancelar:
    Pone fin a la conversación que está en curso. Esta función es compartida entre todos
    los flujos de conversaciones
"""
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await (update.message.reply_text(responses[DEFAULT_LENG]["smsh_end"]))
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
app.add_handler(CommandHandler("commands", commands))
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("privacy", privacy))
app.add_handler(sms_text_handler)
app.add_handler(MessageHandler(filters.ALL, unknown))   # Es el handler por defecto, debe ser el último

# Comienza el bucle de eventos
app.run_polling()

