import os
import re
import torch
import json
import spacy

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
    embeddings = [float(emb) for emb in embeddings] 

    # Normalizar los embeddings
    norm_embeddings = normalize(embeddings, norm='l2')

    return {
            "embeddings": embeddings,
            "norm_embeddings": norm_embeddings
            }



# Endpoint que devuelve entidades y diferentes artefactos presentes en un mensaje; como urls, correos, telefonos...
@app.post("/entity")
def smsh_artifacts(req: Request):
    msg = req.msg
    results = {
        "emails": set(),
        "phones": set(),
        "urls": set(),
        "orgs": set(),
        "persons": set()
        }
    
    # SpaCy NER
    doc = ner(msg)

    # Obtención de artefactos
    for token in doc:
        if(token.like_url):
            results["urls"].add(token.text)
        elif (token.like_email):
            results["emails"].add(token.text)

    # Obtención de entidades (solo ORG y PERSON)
    for ent in doc.ents:
        if(ent.label_ == "ORG"):
            results["orgs"].add(ent.text)
        elif(ent.label_ == "PERSON"):
            results["persons"].add(ent.text)

    return results
