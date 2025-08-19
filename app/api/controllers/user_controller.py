import bcrypt
import logging
import os

from typing import Dict
from fastapi import HTTPException, status
from pydantic import ValidationError
from pymongo.errors import DuplicateKeyError, ConnectionFailure

from models.user import User, UserRequest, RegisterRequest
from exceptions.db_exceptions import DatabaseLoadError
from exceptions.user_exceptions import WrongCredentialsError
from utils.user_utils import generate_nist_password
from utils.email_utils import send_email
from templates.email_templates import PASSWD_EMAIL_TEMPLATE
from dotenv import load_dotenv


# Obtener el logger
logger = logging.getLogger("API")

# Cargar el .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
SMTP_PASSWD = os.getenv("SMTP_PASSWD")
SMTP_SRC = os.getenv("SMTP_SRC")


"""
    Función que permite hacer login con un usuario
"""
async def validate_user(usr) -> Dict:
    user = await User.find_one({"username": usr.username})

    # Comprobar que existe el usuario
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials", headers={"WWW-Authenticate": "Bearer"})
        
    # Comprobar que la contraseña es correcta
    match = bcrypt.checkpw(usr.password.encode('utf-8'), user.password.encode('utf-8'))
    if not match:
        raise HTTPException(status_code=401, detail="Invalid Credentials", headers={"WWW-Authenticate": "Bearer"})
    
    return {
            "token": "TokenDePrueba",
            "user": {
                "name": user.username,
                "surname": user.surname,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "rol": user.rol
                }
            }


"""
    Función para registrar un nuevo usuario
"""
async def register_user(usr) -> bool:
    # Generar Contraseña
    passwd = generate_nist_password()
    hashpass = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt(10)).decode("utf-8")

    # Guardar nuevo usuario
    try:
        user = User(
            name = usr.name,
            surname = usr.surname,
            username = usr.username,
            password= hashpass,
            email= usr.email,
            phone= usr.phone,
            rol= usr.rol,
        )

        await User.insert_one(user)

        send_email(
                src = SMTP_SRC,
                dst = usr.email ,
                topic = PASSWD_EMAIL_TEMPLATE['topic'],
                body = PASSWD_EMAIL_TEMPLATE['body'].format(
                    nombre=usr.name,
                    username=usr.username,
                    password=passwd
                ),
                password_smtp = SMTP_PASSWD
            )

        return True

    except ValidationError as e:
        logger.error(f"Error de validación del documento: {e}")
        raise DatabaseLoadError(f"Error de validación del documento: {e}")
    except DuplicateKeyError as e:
        logger.error(f"Documento duplicado: {e}")
        raise DatabaseLoadError(f"Documento duplicado: {e}")
    except ConnectionFailure as e:
        logger.error(f"No se pudo conectar a la base de datos: {e}")
        raise DatabaseLoadError(f"No se pudo conectar a la base de datos: {e}")
    except Exception as e:
        logger.error(f"Ocurrió un error inesperado: {e}")
        raise DatabaseLoadError(f"Ocurrió un error inesperado: {e}")


async def change_user_passwd(username, old_passwd, new_passwd) -> bool:
    # Validar user-passwd
    user = await User.find_one({"username": username})

    # Comprobar que existe el usuario
    if not user:
        raise WrongCredentialsError("Credenciales no válidas")
        
    # Comprobar que la contraseña es correcta
    match = bcrypt.checkpw(old_passwd.encode('utf-8'), user.password.encode('utf-8'))
    if not match:
        raise WrongCredentialsError("Credenciales no válidas")

    # Cambiar contraseña
    hashpass = bcrypt.hashpw(new_passwd.encode('utf-8'), bcrypt.gensalt(10)).decode("utf-8")
    user.password = hashpass
    await user.save()

    return True
    
