import os
import torch
import json

from pydantic import BaseModel
from fastapi import FastAPI
from simpletransformers.classification import ClassificationModel

# API
app = FastAPI()

# Cargar el modelo
model = None
classes = None

# Modelo para el cuerpo de los requests
class Request(BaseModel):
    msg: str

# Acciones a realizar al levantar la API
@app.on_event("startup")
def app_init():
    global model
    global classes

    model_path = '/home/vboxuser/Downloads/BERT_170625_223642_7_CLASSES'

    use_cuda = torch.cuda.is_available()
    model = ClassificationModel('bert', model_path, use_cuda=use_cuda)

    # Obtener el mapa de clases
    with open(f"{model_path}/training_args.json", "r") as f:
        classes = json.load(f)['labels_map']
    classes = {v: k for k, v in classes.items()}    # Invertir el orden

# Endpoint que comprueba el mensaje
@app.post("/check")
def smhs_type(req: Request):
    print("Dentro")

    msg = [req.msg]

    print("A ver que dice...")

    predictions, raw_outputs = model.predict(msg)

    # Convertir tensores a listas
    # raw_outputs = [output.tolist() for output in raw_outputs]

    # Sacar la predicción y convertirla a texto con el mapa de clases
    predictions = classes[predictions.tolist()[0]]

    return {
            "predictions": predictions
            # "outputs": raw_outputs
            }
