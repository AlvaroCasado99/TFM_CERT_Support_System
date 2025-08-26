#responses = {
#    "es": {
#        "greetings": "¡Hola! Bienvenido/a, ",
#        "rules": """Para interactuar conmigo, ten en cuenta estas reglas:
#
#1. Todas las acciones requieren un comando que debe comenzar con "/". Es muy importante escribirlo así para que pueda ayudarte.
#
#2. Para usar un comando, solo envíalo y sigue las instrucciones que te daré.
#
#3. Los mensajes que detecte como fraude serán almacenados para mejorar mi análisis. No te preocupes, no guardaré ninguna información personal, solo el contenido del mensaje.
#
#4. Puede consultar la política de privacidad de este bot escribiendo el comando: /privacy.
#""",
#        "commands": """ Aquí tienes una lista con comandos útiles:
#
#/sms: inicia el análisis de un mensaje de texto sospechoso.
#/commands: muestra la lista de comandos disponibles con una breve descripción.
#/help: muestra nuevamente estas reglas para interactuar conmigo.
#/privacy: muestra la política de privacidad de esta aplicación.
#""",
#        "ia_act": """¡IMPORTANTE!
#Este bot utiliza un sistema de inteligencia artificial para analizar los mensajes que le envíe. El análisis tiene únicamente carácter informativo y no sustituye el contacto con su banco, proveedor de servicios o autoridad competente. No comparta información personal sensible más allá del mensaje sospechoso que desee analizar.
#""",
#        "privacy": """Política de privacidad
#El presente sistema (aplicación web y bot de Telegram) tiene como finalidad detectar y analizar mensajes sospechosos de smishing con fines de concienciación y ciberseguridad.
#
#Responsable del tratamiento: Álvaro Casado Miguelez.
#
#Datos tratados:
#
#En la aplicación web: credenciales de acceso (nombre de usuario, contraseña cifrada, correo electrónico, rol de usuario) y registros de actividad.
#
#En el bot: mensajes de texto enviados por el usuario, que pueden incluir direcciones URL o direcciones de correo electrónico.

#Finalidad del tratamiento: ofrecer al usuario un análisis del mensaje y estadísticas agregadas sobre intentos de fraude. Los datos no se emplean con fines comerciales ni publicitarios.
#
#Base jurídica: interés legítimo en la prevención del fraude y la seguridad (art. 6.1.f RGPD).
#
#Conservación: los datos se conservarán el tiempo estrictamente necesario para el análisis y la generación de estadísticas, eliminándose o anonimizándose posteriormente.
#
#Destinatarios: no se cederán datos a terceros salvo obligación legal.
#
#Derechos de los usuarios: en cualquier momento puede ejercitar sus derechos de acceso, rectificación, supresión, limitación, oposición y portabilidad enviando una solicitud a [correo de contacto].
#
#Medidas de seguridad: las contraseñas se almacenan mediante algoritmos de hash con salting; las comunicaciones están cifradas con TLS/SSL; el acceso a los datos se controla mediante roles.
#"""
#        "unknown": "Lo siento, no entendí tu mensaje. Recuerda que puedes consultar la lista de comandos escribiendo /help.",
#        "smsh_ready": "¡Perfecto! Estoy listo para analizar el SMS sospechoso que me envíes.",
#        "smsh_go": "Mensaje recibido, comenzando el análisis ahora mismo.",
#        "smsh_result": "Aquí tienes el resultado de mi análisis:",
#        "smsh_end": "Análisis completado. ¿En qué más puedo ayudarte?",
#        "smsh_flavour": "Este mensaje parece un intento de fraude de tipo $$FLAVOUR$$. Este método es comúnmente usado por estafadores para engañar a las personas.",
#        "smsh_entity": "Además, se menciona a la entidad $$ENTITY$$. Si no tienes relación con esta entidad, es muy probable que se trate de una estafa.",
#        "smsh_entities": "Además, se mencionan las entidades $$ENTITIES$$. Si no tienes relación con ninguna de ellas, es muy probable que se trate de una estafa.",
#        "smsh_url": "He detectado una URL en el mensaje. Es fundamental que no hagas clic en ella a menos que estés completamente seguro/a de su legitimidad. Los estafadores suelen crear páginas web muy similares a las reales para robar datos o incluso pueden instalar virus en tu dispositivo.",
#        "smsh_warn": "Si quieres asegurarte o tienes relación con la entidad mencionada, contacta directamente con ellos usando un número o página oficial, no uses los datos que vienen en el mensaje. Busca en internet la información oficial para verificar.",
#        "smsh_safe": "Tras analizar el mensaje, no he encontrado indicios de fraude o smishing. Todo parece seguro. Aun así, recuerda que siempre es buena idea mantenerse atento/a y no compartir información personal si no estás completamente seguro/a del remitente.",
#        "smsh_error": "Lo siento, en este momento no puedo conectarme con el servicio de análisis y no puedo procesar tu mensaje. Por favor, inténtalo de nuevo más tarde."
#    }
#i}

responses = {
    "es": {
        "greetings": "¡Hola! Bienvenido/a, ",
        "rules": """Para interactuar conmigo, ten en cuenta estas reglas:

1. Todas las acciones requieren un comando que debe comenzar con "/". Es muy importante escribirlo así para que pueda ayudarte.

2. Para usar un comando, solo envíalo y sigue las instrucciones que te daré.

3. Los mensajes que se detecten como fraude podrán almacenarse temporalmente para mejorar el análisis. No recogeré más datos que el contenido que envíes y metadatos técnicos mínimos. Si el mensaje contiene datos personales, se tratarán conforme a la política de privacidad y se anonimizarán o eliminarán cuando dejen de ser necesarios.

4. Puedes consultar la política de privacidad escribiendo el comando: /privacy.
""",
        "commands": """Aquí tienes una lista con comandos útiles:

/sms: inicia el análisis de un mensaje de texto sospechoso.
/commands: muestra la lista de comandos disponibles con una breve descripción.
/help: muestra nuevamente estas reglas para interactuar conmigo.
/privacy: muestra la política de privacidad de esta aplicación.
""",
    "ia_act": """¡IMPORTANTE!:

Este bot utiliza un sistema de inteligencia artificial para analizar los mensajes que le envíes. El análisis tiene únicamente carácter informativo y no sustituye el contacto con tu banco, proveedor de servicios o autoridad competente. No compartas información personal sensible más allá del mensaje sospechoso que desees analizar.
""",
    "privacy": """Política de privacidad:

El presente sistema (aplicación web y bot de Telegram) tiene como finalidad detectar y analizar mensajes sospechosos de smishing con fines de concienciación y ciberseguridad.

Responsable del tratamiento: Álvaro Casado Miguelez — Contacto: [acasam@antismish.es].

Datos tratados:
- En la aplicación web: credenciales de acceso (nombre de usuario, contraseña cifrada, correo electrónico, rol de usuario) y registros de actividad.
- En el bot: mensajes de texto enviados por el usuario, que pueden incluir direcciones URL o direcciones de correo electrónico. No se emplean datos con fines publicitarios.

Finalidad del tratamiento: ofrecer al usuario un análisis del mensaje y elaborar estadísticas agregadas sobre intentos de fraude.

Base jurídica: interés legítimo en la prevención del fraude y la seguridad (art. 6.1.f RGPD).

Conservación: los datos se conservarán el tiempo estrictamente necesario para el análisis y la generación de estadísticas, eliminándose o anonimizándose posteriormente.

Destinatarios: no se cederán datos a terceros salvo obligación legal.

Derechos de los usuarios: puede ejercer sus derechos de acceso, rectificación, supresión, limitación, oposición y portabilidad enviando una solicitud a [legal@antismish.es]. También puede retirar su consentimiento cuando proceda y presentar una reclamación ante la AEPD.

Medidas de seguridad: las contraseñas se almacenan mediante algoritmos de hash con salting; las comunicaciones de la aplicación web están cifradas con TLS/SSL; el acceso a los datos se controla mediante roles.
""",
        "unknown": "Lo siento, no entendí tu mensaje. Recuerda que puedes consultar la lista de comandos escribiendo /help.",
        "smsh_ready": "¡Perfecto! Estoy listo para analizar el SMS sospechoso que me envíes.",
        "smsh_go": "Mensaje recibido, comenzando el análisis ahora mismo.",
        "smsh_result": "Aquí tienes el resultado de mi análisis:",
        "smsh_end": "Análisis completado. ¿En qué más puedo ayudarte?",
        "smsh_flavour": "Este mensaje parece un intento de fraude de tipo $$FLAVOUR$$. Este método es comúnmente usado por estafadores para engañar a las personas.",
        "smsh_entity": "Además, se menciona a la entidad $$ENTITY$$. Si no tienes relación con esta entidad, es muy probable que se trate de una estafa.",
        "smsh_entities": "Además, se mencionan las entidades $$ENTITIES$$. Si no tienes relación con ninguna de ellas, es muy probable que se trate de una estafa.",
        "smsh_url": "He detectado una URL en el mensaje. Es fundamental que no hagas clic en ella a menos que estés completamente seguro/a de su legitimidad. Los estafadores suelen crear páginas muy similares a las reales para robar datos o incluso instalar software malicioso en tu dispositivo.",
        "smsh_warn": "Si quieres asegurarte o tienes relación con la entidad mencionada, contacta directamente con ellos utilizando un número o página oficiales; no uses los datos que figuran en el mensaje.",
        "smsh_safe": "Tras analizar el mensaje, no he encontrado indicios de fraude o smishing. Aun así, permanece atento/a y evita compartir información personal si no estás completamente seguro/a del remitente.",
        "smsh_error": "Lo siento, en este momento no puedo conectarme con el servicio de análisis y no puedo procesar tu mensaje. Por favor, inténtalo de nuevo más tarde."
    }
}
