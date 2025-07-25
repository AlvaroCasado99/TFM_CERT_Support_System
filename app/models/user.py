from pydantic import BaseModel
from beanie import Document
from typing import Optional
from pymongo import IndexModel


"""
    Modelo para las request de Login de los usuarios
"""
class UserRequest(BaseModel):
    username: str
    password: str

"""
    Modelo para los usuarios de la base de datos
"""
class User(Document):
    name: str
    surname: str
    username: str
    password: str
    email: str
    phone: Optional[str] = ""
    rol: str = "user"

    class Settings:
        name = "users"   # Nombre de la coleccion en mongo
        indexes = [
            IndexModel([("username", 1)], unique=True),
            IndexModel([("email", 1)], unique=True)
        ]

