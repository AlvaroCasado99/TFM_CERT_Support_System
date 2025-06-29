from fastapi import APIRouter
from pydantic import BaseModel
from app.models.issue import Issue

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

    issue = Issue()

    issue.msg = item.msg

    # Conocer el tipo de smishing
    issue.flavour = "Preguntar a BERT"
    
    # Buscar entidades en el mensaje
    issue.entity = "Preguntar a un NER"

    # Identificar URL, MAIL, PHONE
    issue.url = "Buscar con regex o con NER"
    issue.mail = "Buscar con regex o con NER"
    issue.phone = "Buscar con regex o con NER"

    # Obtener código HTML de la URL
    if issue.mail:
        issue.html = "Lo que nos devuelva el DOCKER"

    # Extraer los embeddings del mensaje con BERT

    # Pasar por función de similitud
    # Comparar con otras de la base de datos
    # Obtener y guardar el ID de la campaña

    # Subir a la base de datos la ISSUE

    # Genrerar un reporte
    #report = issue.report_basic()
    
    return {
            "msg": item.msg,
            "issue": issue.to_dict()
            }
