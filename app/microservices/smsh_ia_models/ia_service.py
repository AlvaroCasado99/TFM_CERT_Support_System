import os
import torch
import json

from pydantic import BaseModel
from fastapi import FastAPI

from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModelForSequenceClassification
from transformers import pipeline

from sentence_transformers import SentenceTransformer

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

    # Cargar modelo NER
    tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
    ner_model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
    ner = pipeline("ner", model=ner_model, tokenizer=tokenizer)

    # Cargar modelo de Embeddings
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Endpoint que comprueba el mensaje
@app.post("/check")
def smhs_type(req: Request):
    msg = [req.msg]

    predictions = classificator(msg)
    predicted_class = classes[int(predictions[0]['label'].split('_')[1])]

    return {
            "predictions": predicted_class
            }


# Endpoint que busca entidades dentro de un mensaje
@app.post("/entity")
def snsh_ner(req: Request):
    msg = req.msg

    results = ner(msg)
    
    return {
            "entities": results
            }


# Endpoint que devuleve los embeddings semánticos de un texto para futuras comparaciones
@app.post("/embedding")
def smsh_embedding(req: Request):
    msg = req.msg

    embeddings = embedder.encode([msg], convert_to_tensor=False)[0] # Devuelve un tensor en formato de lista
    embeddings = [float(emb) for emb in embeddings] 
    return {
            "embeddings": embeddings
            }
