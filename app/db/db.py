import os
from dotenv import load_dotenv

from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.smishing import Smishing
from app.models.user import User

# Cargar el .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# Función para inicializar la conexión con Mongo a través de Beanie
async def init_db():
    client = AsyncIOMotorClient(MONGO_URI)
    await init_beanie(database=client["Phishing"], document_models=[Smishing, User])
