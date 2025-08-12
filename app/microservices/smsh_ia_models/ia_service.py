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

#from logger_config.setup_logger import setup_logger

# API
app = FastAPI()

# Logger
#logger = setup_logger("MS1", "ia_service.log", "./logs")
#logger.info("Arrancando el servicio MS1 (IA)")

# Cargar el modelos
embedder = None
ner = None
class_bin = None
class_7c = None
class_13c = None

#classificator = None
#classes = None

# Modelo para el cuerpo de los requests
class Request(BaseModel):
    msg: str


# Objeto clasificado
class Classifier():

    """ Constructor """
    def __init__(self, model_path:str="./bert_classifier", tokenizer:bool=False):
        self.model_path=model_path
        self.tokenizer_path=model_path if tokenizer else "bert-base-uncased"

        # Inicializamos al crear la instancia
        self.classifier = self._load_classifier()
        self.id2label = self._load_id2label()

    def _load_classifier(self):
        model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
        tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path)
        tokenizer.model_max_length = 256
        return pipeline("text-classification", model=model, tokenizer=tokenizer)

    def _load_id2label(self):
        with open(f"{self.model_path}/config.json", "r") as f:
            return json.load(f)['id2label']

    """ Predecir mensajes """
    def classify(self, msg: str=""):
        #predictions = self.classifier(msg, truncation=True, max_length=256, padding=True)
        predictions = self.classifier(msg)
        print(predictions)
        label = predictions[0]['label']
        return label


# Acciones a realizar al levantar la API
@app.on_event("startup")
def app_init():
    #global classificator
    #global classes
    global ner
    global embedder
    global class_bin
    global class_7c
    global class_13c

    
    # Cargar modelo clasificador
#    model_path = './bert_classifier'
#    tokenizer = AutoTokenizer.from_pretrained(model_path)
#    class_model = AutoModelForSequenceClassification.from_pretrained(model_path)
#    classificator = pipeline("text-classification", model=class_model, tokenizer=tokenizer)

    # Obtener el mapa de clases
#    with open(f"{model_path}/config.json", "r") as f:
#        classes = json.load(f)['labels_list']

    # Cargar modelos de clasificación
    class_bin = Classifier(model_path = "./bert_binary")
    class_7c = Classifier(model_path = "./bert_classifier_7c")
    class_13c = Classifier(model_path = "./bert_classifier_13c")

    # Cargar modelo de Embeddings
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    # Cargar modelo NER SPACY para entidades y artefactos
    ner = spacy.load("en_core_web_sm")



# Endpoint que comprueba el mensaje
@app.post("/check")
def smhs_type(req: Request):
#    msg = [req.msg]
#    predictions = classificator(msg)
#    predicted_class = classes[int(predictions[0]['label'].split('_')[1])]

    pred_bin = class_bin.classify(msg=req.msg)
    pred_7c = "ham"
    pred_13c = "ham"

    if not pred_bin == "ham":
        pred_7c = class_7c.classify(msg=req.msg)
        pred_13c = class_13c.classify(msg=req.msg)

    return {
            "result": {
                    "7c": pred_7c,
                    "13c": pred_13c
                }
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
            "result": {
                    "embeddings": embeddings.tolist(),
                    "norm_embeddings": norm_embeddings[0].tolist()
                }
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
    if results['url']:
        results['url'] = list(results['url'])[0]
    else:
        results['url'] = ""

    if results['email']:
        results['email'] = list(results['email'])[0]
    else:
        results['email'] = ""
        
    #results["url"] = results['url'] ? list(results["url"])[0] : ""
    #results["email"] = results['email'] ? list(results["email"])[0] : ""

    # Obtención de entidades (solo ORG y PERSON)
    for ent in doc.ents:
        if(ent.label_ == "ORG"):
            results["org"].add(ent.text)
        elif(ent.label_ == "PERSON"):
            results["person"].add(ent.text)

    return {
            "result": results
            }
