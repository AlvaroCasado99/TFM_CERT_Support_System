responses = {
    "es": {
        "greetings": "Bienvenido ",
        "rules": """Estas son las reglas para poder interactuar conmigo:
1. Todas las acciones necesitan un comando. Todos los comandos van precedidos por /, es muy importante que lo escribas o no podré ayudarte. Podrás ver la lista de comandos a continuación.
2. Para usar los comandos solo tienes que enviar un mensaje con el comando y seguir las instrucciones.
3. Los mensajes que sean identificados como 'fraude' se registrarán en la base de datos para poder mejorar mis capacidades. No te preocupes, nigún tipo de información relacionada contigo será guardada, solo el mensaje.
        """,
        "commands": """/sms: para iniciar el proceso de análisis de un mensaje de texto.
/commands: para volver a ver la lista de comandos disponibles con una breve descripción.
/help: muestra las reglas para interactuar conmigo.
        """,
        "unknown": "Lo siento, no entiendo lo que me quieres decir. Recuerda que puedes consular la lista de comandos escribiendo /help.",
        "smsh_ready": "Entendido! Estoy listo para analizar el SMS sospechoso.",
        "smsh_go":"Recibido, me pondré con ello ahora mismo.",
        "smsh_result": "Esto es lo que lo que he encontrado:",
        "smsh_end": "Conversación terminada, ¿en que puedo ayudarte?",
        "smsh_flavour":  "Parece que se trata de un mensaje frauduleto de tipo $$FLAVOUR$$, es muy comun que los estafadores usen esto como excusa. ",
        "smsh_entity": "Además, en el mensaje se menciona a $$ENTITY$$. Esta es la primera pista, si no tienes relación con esta entidad puedes estar seguro de que se trata de una estafa. ",
        "smsh_entities": "Además, en el mensaje se mencionan a $$ENTITIES$$. Esta es la primera pista, si no tienes relación con ninguna de estas entidades puedes estar seguro de que se trata de una estafa. ",
        "smsh_url": "Veo también que en el mensaje hay una URL, es fundamental que no accedas a ella a menos que sepas que el mensaje el legítimo. Los estafadores suelen imitar muy bien páginas web lo cual les permite robar contraseñas. También existe la posibilidad que al entrar se descargue un archivo que contenga un virus. ",
        "smsh_warn": "Si por el contrario sí estas relacionanado o quieres asegurarte, siempre puedes ponerte en contacto con ellos para comprobarlo. MUY IMPORTANTE, no utilices el número que te envió el mensaje o cualquier otro medio que aparezca en el mensaje. Busca en Google la página de esta empresa y usa el teléfono de atención al cliente que ahí te indiquen.",
    }
}
