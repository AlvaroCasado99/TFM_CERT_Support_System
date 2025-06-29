# TFM_CERT_Support_System

# Para lanzar la base de datos mongo
1. Ir a *app/*
2. Levantar el contenedor: *docker compose up -d* 

# Para lanzar la API en local con UVICORN:
1. Ir a la carpeta raíz
2. Ejecutar el comando: *python3 main.py*

o también:
1. Ir a la carpeta raíz
2. Lanzar el comando:  *uvicorn app.api.main:app --reload*
    **app.api.main** -> Es la ruta al MAIN de la API
    **:app** -> Es el nombre de la instancia de FastAPI en el main.py
    **--reload** -> Permite que se recargue el servidor cuando detecte cambios en el código fuente

# ¿Cómo funciona?
Arquitectura:
1. API principal (Host)
2. Base de datos Mongo (Docker)
3. Nginx (Host)
4. Microservicio 1: Smishing Type (Docker)
5. Microservicio 2: NER Detection (Docker)
6. Microservicio 3: Deteccion de URL, Mail, Phone... (Docker)
7. Microservicio 4: Obtención de código HTML (Docker)
8. Microservicio 5: Función de similitud de campañas (Docker)
