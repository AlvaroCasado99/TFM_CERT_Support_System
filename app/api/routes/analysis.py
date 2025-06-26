from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# Modelo para el cuerpo de los requests
class Item(BaseModel):
    msg: str | list[str]

# Endpoint de prueba para este router
@router.get("/test")
def get_analysis_test():
    return {
            "message": "Router /analysis funciona!"
            }


# Endpoint para crear reportes BASICOS de mensajes de texto
@router.post("/text/basic")
def generate_basic_report(item: Item):
    return {
            "msg": item.msg
            }
