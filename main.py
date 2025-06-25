# IMPORTANTE
# Este debe ser el punto de entrada a la aplicacaión (la raíz).
# Usar 'uvicorn' para lanzar la API y el BOT ejecuatando cada 'main.py'

import uvicorn

# Ejemplo
if __name__ == "__main__":
    uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=True)
