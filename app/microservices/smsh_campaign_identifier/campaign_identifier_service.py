import os

import numpy as np

from faiss import IndexFlatIP
from pydantic import BaseModel
from fastapi import FastAPI

from models.smishing import Smishing


# API
app = FastAPI()

# Indice de búsqueda FAISS
index = None
db_embeddings = None

# Modelo para el cuerpo de los requests
class Request(BaseModel):
    embedding: list[float]


# Acciones a realizar al levantar la API
@app.on_event("startup")
async def app_init():
    global index
    global db_embeddings

    # Obtener los embeddings normalizados de la base de datos
    #db_embeddings = await Smishing.find().to_list()
    #embeddings = [doc["norm_embeddings"] for doc in db_embeddings]

    #embeddings_np = np.array(embeddings).astype("float32")
    #index = IndexFlatIP(embeddings_np.shape[1])
    #index.add(embeddings_np)


# Endpoint que comprueba el mensaje
@app.post("/campaign")
def smhs_type(req: Request):
    embedding = [req.embedding] # Debe ser el vector normalizado

    return {
            "campaign": "@ilmzdf54zdf54"
            }

    # Buscar los 5 más similares
    head = 5
    D, I = index.search(embedding, head)

    # Comprobar la campaña más representada con una consulta 
    print(D)
    print(I)
    for i, (score, idx) in enumerate(zip(D[0], I[0])):
        print(f"{i+1}. Score: {score:.4f} | ID: {db_embeddings['_id'][idx]}")

    # Filtrar por umbral
    threshold = 0.85

    # La más representada será la elegida, si no hay ninguna se genera una nueva
    

    return {
            "campaign": "La de verano"
            }
