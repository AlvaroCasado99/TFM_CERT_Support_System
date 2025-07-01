import os
# import torch

from pydantic import BaseModel
from fastapi import FastAPI
# from simpletransformers.classification import ClassificationModel

# API
app = FastAPI()

# Cargar el modelo
model = None

# Modelo para el cuerpo de los requests
class Request(BaseModel):
    msg: str

# Acciones a realizar al levantar la API
@app.on_event("startup")
def app_init():
    global model
    # use_cuda = torch.cuda.is_available()
    # model = ClassificationModel('bert', 'ruta/al/modelo/guardado', use_cuda=use_cuda)

# Endpoint que comprueba el mensaje
@app.post("/check")
def smhs_type(req: Request):
    msg = [req.msg]

    # predictions, raw_outputs = model.predict(msg)

    return {
            "entity": "Santander"
            }
