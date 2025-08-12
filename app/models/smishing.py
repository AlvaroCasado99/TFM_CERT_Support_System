from pydantic import BaseModel, Field
from beanie import Document, PydanticObjectId
from typing import Optional
from bson import ObjectId
from datetime import datetime

class Smishing(Document):
    msg: str
    flavour: str
    flavour_13c: str
    entity: Optional[str] | Optional[list]
    url: Optional[str]
    mail: Optional[str]
    phone: Optional[str]
    html: Optional[str]
    embeddings: list
    norm_embeddings: list
    campaign: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "smishing"   # Nombre de la coleccion en mongo


class SmishingProjectionFAISS(BaseModel):
    #id: PydanticObjectId = Field(alias="_id")
    norm_embeddings: list
    campaign: str

class SmishingProjectionGraphCategory(BaseModel):
    flavour: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SmishingProjectionGraphOrganizationCategory(BaseModel):
    flavour: str
    entity: Optional[str] | Optional[list]
    #created_at: datetime = Field(default_factory=datetime.utcnow)

class SmishingProjectionGraphMessages(BaseModel):
    msg: str
