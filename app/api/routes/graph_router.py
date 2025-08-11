from fastapi import APIRouter, HTTPException, status
from app.models.requests import GraphRequest
import app.api.controllers.graph_controller as gc

# Router
router = APIRouter()

# Endpoint de prueba para este router
@router.get("/test")
def get_analysis_test():
    return {
            "message": "Router /graph funciona!"
            }

# Endpoint para obtener los datos usados en un grafico PIE de categorias
@router.post("/msg_categories")
async def graph_msg_category(req: GraphRequest):
    return await gc.get_graph_message_category_data(
            start=req.start, 
            end=req.end
        )

# Endpoint para obetener datos usados en un gráfico STACKED BAR. El gráfico cuenta con 
# categorías agrupadas por plazos de tiempo.
@router.post("/stack_bar_time_categories")
async def graph_stack_bar_time_categories(req: GraphRequest):
    return await gc.get_stacked_bar_time_categories_data(
            start=req.start,
            end=req.end,
            interval=req.interval
        )

# Endpoint para obetener datos usados en un gráfico STACKED HORIZONTAL BAR.
# El gráfico muestra las empresas más comunes y en que tipo de mensajes aparecen.
@router.post("/categories_organizations")
async def graph_stack_hbar_categories_organizations(req: GraphRequest):
    return await gc.get_stacked_barh_categories_organizarions_data(
            start=req.start, 
            end=req.end
        )

# Endpoint
# Este endpoint devuelve todos los mensajes dentro de un periodo dado juntos
# para posteriormente usarse en un wordcount
@router.post('/smishing_messages')
async def graph_smishing_messages(req: GraphRequest):
    return await gc.get_graph_messages_data(
            start=req.start, 
            end=req.end
        )
