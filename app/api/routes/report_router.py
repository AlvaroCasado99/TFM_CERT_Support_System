from fastapi import APIRouter

from app.models.requests import Report

from app.api.controllers.report_generator_controller import advanced_report_generator

# Router
router = APIRouter()


# Endpoint de prueba para este router
@router.get("/test")
def get_analysis_test():
    return {
            "message": "Router /report funciona!"
            }


# Endpoint para análisis AVANZADO de mensajes de texto
@router.post("/advanced")
def generate_advanced_report(report: Report):
    return advanced_report_generator(report)
