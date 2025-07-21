import os

import numpy as np

from faiss import IndexFlatIP
from pydantic import BaseModel
from fastapi import FastAPI

from models.smishing import Smishing, SmishingProjectionFAISS

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, PydanticObjectId


# API
app = FastAPI()

# Indice de búsqueda FAISS
index = None
db_embeddings = None

# Modelo para el cuerpo de los requests
class Request(BaseModel):
    embedding: list[float]

# Modelo para actualizar indices
class IndexRequest(BaseModel):
    id: str
    norm_embeddings: list[float]
    campaign: str


# Acciones a realizar al levantar la API
@app.on_event("startup")
async def app_init():
    global index
    global db_embeddings

    # Iniciar Beanie
    client = AsyncIOMotorClient("mongodb://mongo:27017/")
    await init_beanie(database=client["Phishing"], document_models=[Smishing])

    # Obtener los embeddings normalizados de la base de datos
    db_embeddings = await Smishing.find({}).project(SmishingProjectionFAISS).to_list()

    # Solo crear el índice si hay datos en la BBDD 
    if db_embeddings:
        embeddings = [doc.norm_embeddings for doc in db_embeddings]
        embeddings_np = np.array(embeddings).astype("float32")
        index = IndexFlatIP(embeddings_np.shape[1])
        index.add(embeddings_np)


# Endpooint para comprobar que esta activo
@app.post("test")
def test_api():
    return {
            "response": "La API para campañas esta activa"
            }

# Endpoint para actualizar el índice con un nuevo mensaje
def update_index(req: IndexRequest):
    # Actualizo el array de la base de datos
    db_embeddings.append(
            SmishingProjectionFAISS(
                    id=req.id,
                    norm_embeddings=req.norm_embeddings,
                    campaign=req.campaign
                )
        )

    # Actualizo el índice
    index.add(req.norm_embeddings)


# Endpoint que comprueba el mensaje
@app.post("/campaign")
def smhs_type(req: Request):
    embedding = np.array([req.embedding]).astype("float32") # Debe ser el vector normalizado

    # Si la base de datos esta vacía
    if index==None and not db_embeddings:
        return {"campaign": str(PydanticObjectId())}

    # Buscar los 5 más cercanos
    campaign = ""
    threshold = 0.85
    k = 5
    D, I = index.search(embedding, k)

    # Comprobar la campaña más representada con una consulta
    search_results = zip(D[0], I[0])
    best_idx = I[0][0]
    best_score = [0][0] 

    # Filtrar por umbral
    if best_score >= threshold:
        campaign = db_embeddings[best_idx].campaign
    else:
        campaign = str(PydanticObjectId())

    return {
            "campaign": campaign
            }
