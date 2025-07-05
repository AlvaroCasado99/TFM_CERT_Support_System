from pydantic import BaseModel
from typing import Optional

# Modelo para requests de ANÁLISIS DE TEXTO
class Item(BaseModel):
    msg: str | list[str]


"""
    Modelo para los requests de ADVANCED REPORT
"""
class Report(BaseModel):
    msg: str
    flavour: str
    entity: Optional[str] | Optional[list]
    url: Optional[str]
    mail: Optional[str]
    phone: Optional[str]
    html: Optional[str]
    embeddings: list
    campaign: Optional[str]
