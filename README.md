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
