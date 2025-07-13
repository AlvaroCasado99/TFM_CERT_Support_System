from pydantic import BaseModel
from beanie import Document
from typing import Optional

class Smishing(Document):
    msg: str
    flavour: str
    entity: Optional[str] | Optional[list]
    url: Optional[str]
    mail: Optional[str]
    phone: Optional[str]
    html: Optional[str]
    embeddings: list
    norm_embeddings: list
    campaign: Optional[str]

    class Settings:
        name = "smishing"   # Nombre de la coleccion en mongo

