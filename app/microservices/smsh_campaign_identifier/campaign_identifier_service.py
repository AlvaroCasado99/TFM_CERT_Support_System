import os

import numpy as np

from faiss import IndexFlatIP
from pydantic import BaseModel
from fastapi import FastAPI

from models.smishing import Smishing, SmishingProjectionFAISS
from logger_config.setup_logger import setup_logger

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, PydanticObjectId

from apscheduler.schedulers.asyncio import AsyncIOScheduler


# PRUEBAS
#from pydantic import Field
#from beanie import Document
#from typing import Optional

#class Smishing(Document):
#    msg: str
#    flavour: str
#    entity: Optional[str] | Optional[list]
#    url: Optional[str]
#    mail: Optional[str]
#    phone: Optional[str]
#    html: Optional[str]
#    embeddings: list
#    norm_embeddings: list
#    campaign: Optional[str]
#
#    class Settings:
#        name = "smishing"   # Nombre de la coleccion en mongo


#class SmishingProjectionFAISS(BaseModel):
#    norm_embeddings: list
#    campaign: str





# ------------ VARIABLES --------------
# API
app = FastAPI()

# Logger
logger = setup_logger("MS3", "campaign_service.log", "./logs")
logger.info("Arrancando el servicio MS3 (Campaign)")

# Scheduler
scheduler = AsyncIOScheduler()

# Indice de búsqueda FAISS
index = None
db_embeddings = None
last_synced_id = None
# -------------------------------------




# ------------ MODELOS ----------------
# Modelo para el cuerpo de los requests
class Request(BaseModel):
    embedding: list[float]

# Modelo para actualizar indices
class IndexRequest(BaseModel):
    norm_embeddings: list[float]
    campaign: str
# -------------------------------------




# -------- FUNCIONES INTERNAS ---------
# Función para crear un indice
async def _sync_index_with_database():
    print("[INFO] Sincronizando el índice con la base de datos.")

    global index
    global db_embeddings

    # Obtener los embeddings normalizados de la base de datos
    db_embeddings = await Smishing.find({}).project(SmishingProjectionFAISS).to_list()

    # Solo crear el índice si hay datos en la BBDD 
    if db_embeddings:
        embeddings = [doc.norm_embeddings for doc in db_embeddings]
        embeddings_np = np.array(embeddings).astype("float32")
        index = IndexFlatIP(embeddings_np.shape[1])
        index.add(embeddings_np)

# --------------------------------------



# ------------ ENDPOINTS --------------
# Acciones a realizar al levantar la API
@app.on_event("startup")
async def app_init():
    # Iniciar Beanie
    client = AsyncIOMotorClient("mongodb://mongo:27017/")
    #client = AsyncIOMotorClient("mongodb://localhost:27017/")
    await init_beanie(database=client["Phishing"], document_models=[Smishing])

    # Crear el índice y obtener datos
    await _sync_index_with_database()

    # Scheduler
    scheduler.add_job(_sync_index_with_database, 'interval', seconds=120)
    scheduler.start()


# Acciones a realizar cuando se apaque la api
@app.on_event("shutdown")
def app_end():
    scheduler.shutdown()


# Endpooint para comprobar que esta activo
@app.post("/test")
def test_api():
    return {
            "response": "La API para campañas esta activa"
            }

# Endpoint para actualizar el índice con un nuevo mensaje
@app.post("/update")
def update_index(req: IndexRequest):
    print("[INFO] Actualizando el índice y la base de datos local.")
    
    global db_embeddings
    global index

    # Actualizo el array de la base de datos
    db_embeddings.append(
            SmishingProjectionFAISS(
                    norm_embeddings=req.norm_embeddings,
                    campaign=req.campaign
                )
        )

    # Actualizo el índice
    index.add(np.array([req.norm_embeddings]).astype("float32"))

    return {
        "result": "Datos incluidos en el índice correctamente"
            }


# Endpoint que comprueba el mensaje
@app.post("/campaign")
def smhs_type(req: Request):
    embedding = np.array([req.embedding]).astype("float32") # Debe ser el vector normalizado

    # Si la base de datos esta vacía
    if index==None and not db_embeddings:
        return {"campaign": str(PydanticObjectId())}

    # Buscar los 5 más cercanos
    campaign = ""
    threshold = 0.75
    k = 5
    D, I = index.search(embedding, k)

    # Comprobar la campaña más representada con una consulta
    search_results = zip(D[0], I[0])
    
    #for i, (score, idx) in enumerate(search_results):
    #    print(f"{i+1}. Score: {score} | ID: {db_embeddings[idx].id}")

    best_idx = I[0][0]
    best_score = D[0][0] 


    # Filtrar por umbral
    if best_score >= threshold:
        campaign = db_embeddings[best_idx].campaign
    else:
        campaign = str(PydanticObjectId())

    return {
            "result": campaign
            }
