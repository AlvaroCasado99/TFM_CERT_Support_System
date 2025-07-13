import os
import httpx

from pydantic import BaseModel
from fastapi import FastAPI

# API
app = FastAPI()

# Cargar el modelo
model = None

# Modelo para el cuerpo de los requests
class Request(BaseModel):
    url: str

# Endpoint que comprueba la url y devuelve su html
@app.post("/url")
async def smhs_type(req: Request):
    url = req.url
    html = ""
    
    # Comprobar si la URL sigue activa con un tiempo de espera fijo
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                html = response.text
        except httpx.ConnectError as e:
            print(f"Hubo un problema al intentar conectar con {url}: {e}")
        except httpx.UnsupportedProtocol as e:
            print(f"Hubo con el protocolo de la url '{url}': {e}")

    return {
            "html": html
            }
