from pydantic import BaseModel

# Modelo para requests de ANÁLISIS DE TEXTO
class Item(BaseModel):
    msg: str | list[str]
