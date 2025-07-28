import os
import httpx

from pydantic import BaseModel
from fastapi import FastAPI

from logger_config.setup_logger import setup_logger

# API
app = FastAPI()

# Logger
logger = setup_logger("MS2", "html_service.log", "./logs")
logger.info("Arrancando el servicio MS2 (HTML)")

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
            response = await client.get(url, timeout=5.0)
            response.raise_for_status()
            html = response.text
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            logger.info(f"Se recibió el código {status_code} de la url: '{url}'")
            #print(f"[ERROR] Se recibió el código {status_code} de la url: '{url}'")
        except httpx.ConnectError as e:
            logger.info(f"Hubo un problema al intentar conectar con '{url}': {e}")
            #print(f"[ERROR] Hubo un problema al intentar conectar con '{url}': \n{e}")
        except httpx.UnsupportedProtocol as e:
            logger.info(f"Hubo con el protocolo de la url '{url}': {e}")
            #print(f"[ERROR] Hubo con el protocolo de la url '{url}': \n{e}")
        except httpx.ReadTimeout as e:
            logger.info(f"No se pudo conetar con '{url}', se excedió el tiempo de espera. Por favor compruebe su conexión. \n{e}")
            #print(f"[ERROR] No se pudo conetar con '{url}', se excedió el tiempo de espera. Por favor compruebe su conexión. \n{e}")
        except Exception as e:
            logger.info(f"Ha ocurrido un error inseperado al intentar conectar con '{url}': {e}")
            #print(f"[ERROR] Ha ocurrido un error inseperado al intentar conectar con '{url}': \n{e}")

    return {
            "result": html
            }
