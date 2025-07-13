import os

from faiss import IndexFlatIP
from pydantic import BaseModel
from app.models.smishing import Smishing
from fastapi import FastAPI


# API
app = FastAPI()

# Indice de búsqueda FAISS
index = None
db_embeddings = None

# Modelo para el cuerpo de los requests
class Request(BaseModel):
    embedding: list


# Acciones a realizar al levantar la API
@app.on_event("startup")
def app_init():
    # Obtener los embeddings normalizados de la base de datos
    db_embeddings = await Smishin.find().to_list()
    embeddings = db_embeddings["norm_embeddings"]

    # Cargar el indice con todos los embedings de mensajes
    dimension = len(embeddings[0])
    index = IndexFlatIP(dimension)
    index.add(embeddings)


# Endpoint que comprueba el mensaje
@app.post("/campaign")
def smhs_type(req: Request):
    embedding = [req.embedding] # Debe ser el vector normalizado

    # Buscar los 5 más similares
    head = 5
    D, I = index.search(embedding, head)

    # Comprobar la campaña más representada con una consulta 
    print(D)
    print(I)
    for i, (score, idx) in enumerate(zip(D[0], I[0])):
        print(f"{i+1}. Score: {score:.4f} | ID: {db_embeddings['_id'][idx]}")

    # Filtrar por umbral
    threshold = 0.80

    # La más representada será la elegida, si no hay ninguna se genera una nueva
    

    return {
            "campaign": "La de verano"
            }
