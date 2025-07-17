import os
import re
import torch
import json
import spacy

import numpy as np

from pydantic import BaseModel
from fastapi import FastAPI

from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModelForSequenceClassification
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize

# API
app = FastAPI()

# Cargar el modelos
embedder = None
ner = None
classificator = None
classes = None

# Modelo para el cuerpo de los requests
class Request(BaseModel):
    msg: str

# Acciones a realizar al levantar la API
@app.on_event("startup")
def app_init():
    global ner
    global ner2
    global classificator
    global classes
    global embedder
    
    # Cargar modelo clasificador
    model_path = './bert_classifier'
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    class_model = AutoModelForSequenceClassification.from_pretrained(model_path)
    classificator = pipeline("text-classification", model=class_model, tokenizer=tokenizer)

    # Obtener el mapa de clases
    with open(f"{model_path}/training_args.json", "r") as f:
        classes = json.load(f)['labels_list']

    # Cargar modelo de Embeddings
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    # Cargar modelo NER SPACY para entidades y artefactos
    ner = spacy.load("en_core_web_sm")



# Endpoint que comprueba el mensaje
@app.post("/check")
def smhs_type(req: Request):
    msg = [req.msg]

    predictions = classificator(msg)
    predicted_class = classes[int(predictions[0]['label'].split('_')[1])]

    return {
            "predictions": predicted_class
            }



# Endpoint que devuleve los embeddings semánticos de un texto para futuras comparaciones
@app.post("/embedding")
def smsh_embedding(req: Request):
    msg = req.msg
    
    # Obtener los embedings del mensaje
    embeddings = embedder.encode([msg], convert_to_tensor=False)[0] # Devuelve un tensor en formato de lista
    embeddings = np.array([float(emb) for emb in embeddings])

    # Normalizar los embeddings
    norm_embeddings = normalize(embeddings.reshape(1, -1), norm='l2')

    return {
            "embeddings": embeddings.tolist(),
            "norm_embeddings": norm_embeddings[0].tolist()
            }



# Endpoint que devuelve entidades y diferentes artefactos presentes en un mensaje; como urls, correos, telefonos...
@app.post("/entity")
def smsh_artifacts(req: Request):
    msg = req.msg
    results = {
        "email": set(),
        "phone": set(),
        "url": set(),
        "org": set(),
        "person": set()
        }
    
    # SpaCy NER
    doc = ner(msg)

    # Obtención de artefactos
    for token in doc:
        if(token.like_url):
            results["url"].add(token.text)
        elif (token.like_email):
            results["email"].add(token.text)

    # Se espera que solo exista una url/email por mensaje
    results["url"] = list(results["url"])[0]
    results["email"] = list(results["email"])[0]

    # Obtención de entidades (solo ORG y PERSON)
    for ent in doc.ents:
        if(ent.label_ == "ORG"):
            results["org"].add(ent.text)
        elif(ent.label_ == "PERSON"):
            results["person"].add(ent.text)

    return results
