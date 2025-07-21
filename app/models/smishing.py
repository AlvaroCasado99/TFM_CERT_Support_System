from pydantic import BaseModel, Field
from beanie import Document, PydanticObjectId
from typing import Optional
from bson import ObjectId

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


class SmishingProjectionFAISS(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    norm_embeddings: list
    campaign: str

