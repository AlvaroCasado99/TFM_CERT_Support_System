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
        classes = json.load(f)['labels_map']
    classes = {v: k for k, v in classes.items()}    # Invertir el orden

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

    print(f"Estas son las predicciones:\n{predictions}")

    # Sacar la predicción y convertirla a texto con el mapa de clases
    #predictions = classes[predictions.tolist()[0]]

    return {
            #"predictions": predictions
            "predictions": "prueba de predicciones"
            }


# Endpoint que busca entidades dentro de un mensaje
@app.post("/entity")
def snsh_ner(req: Request):
    msg = req.msg

    results = ner(msg)
    
    print(f"Estas son las entidades:\n{results}")

    return {
            #"entities": results
            "entities": "Prueba de entidades"
            }


# Endpoint que devuleve los embeddings semánticos de un texto para futuras comparaciones
@app.post("/embedding")
def smsh_embedding(req: Request):
    msg = req.msg

    embeddings = embedder.encode([msg], convert_to_tensor=False) # Devuelve un tensor en formato de lista
    
    print(f"Estos son los embeddings:\n{embeddings}")

    return {
            #"embeddings": embeddings
            "embeddings": ["prueba", "de", "embedding"]
            }
