import httpx
import logging

from web.utils.constants import API_URL

from typing import Dict, Any, Optional

# Obtener el logger
logger = logging.getLogger("frontend")

class APIClient:

    # Constructor de clase
    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url

    # Función para hacer requests a la API
    def request_data(self, endpoint: str, data: Dict[str, Any], timeout: int = 300) -> Dict[str, Any]:
        try:
            # Lanzar peticion a la API
            with httpx.Client() as client:
                res = httpx.post(
                       f"{self.base_url}/{endpoint}", 
                       json=data, 
                       timeout=timeout
                    )
                res.raise_for_status()
                return {"ok": True,  "data": res.json()}
    
        except httpx.RequestError as e:
            logger.error(f"Request Error: {e}")
            return {"ok": False, "error": "Error de conexión. Inténtelo más tarde."}

        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            logger.error(f"He recogido este error: {status_code} -> {e}")
            if status_code >= 500:
                return {"ok": False, "error": "Error del servidor. Inténtelo más tarde."}
            else:
                return {"ok": False, "error": f"Ha ocurrido un error inesperado ({status_code})."}
        except Exception as e:
            logger.error(f"Ha ocurrido un error inesperado: {e}")
            return {"ok": False, "error": f"Ha ocurrido un error inesperado ({e})."}

    # Función para haer requests 

# Instancia global de APIClient()
api_client = APIClient()
