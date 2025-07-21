from fastapi import APIRouter

from app.models.requests import Item

from app.api.controllers.message_analysis_controller import advanced_text_analysis, db_test

# Router
router = APIRouter()


# Endpoint de prueba para este router
@router.get("/test")
def get_analysis_test():
    return {
            "message": "Router /analysis funciona!"
            }

# DELETE: Endpoint para testear beanie
@router.get("/beanie")
async def beanie_test():
    return await db_test()


# Endpoint para análisis AVANZADO de mensajes de texto
@router.post("/text/advanced")
async def analyse_text_advanced(item: Item):
    return await advanced_text_analysis(item.msg)
