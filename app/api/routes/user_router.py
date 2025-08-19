import logging

from fastapi import APIRouter, HTTPException, status

from models.user import User, UserRequest, RegisterRequest, ChangePasswdRequest
from exceptions.db_exceptions import DatabaseLoadError
from exceptions.user_exceptions import WrongCredentialsError
from controllers.user_controller import validate_user, register_user, change_user_passwd

# Obtener el logger
logger = logging.getLogger("API")

# Router
router = APIRouter()


# Endpoint de prueba para este router
@router.get("/test")
def get_analysis_test():
    return {
            "message": "Router /user funciona!"
            }

"""
    Endpoint 
    Permite autenticar usuarios por contraseña
"""
@router.post("/login")
async def user_login(req: UserRequest):
    logger.info("Nueva petición de login")
    return await validate_user(req)


"""
    Endpoint:
    Permite registrar a un usuario
"""
@router.post("/register")
async def user_register(req: RegisterRequest):
    logger.info("Nueva petición de registro de usuario")
    try:
        return await register_user(req)
    except DatabaseLoadError as e:
        raise HTTPException(status_code=400, detail="No se ha podido crear el usuario.")

"""
    Endpoint:
    Permite al usuario cambiar la contraseña
"""
@router.post("/change_pass")
async def user_change_passwd(req: ChangePasswdRequest):
    logger.info("Nueva petición de cambio de contraseña")
    try:
        return await change_user_passwd(
                username=req.username,
                new_passwd=req.new_passwd, 
                old_passwd=req.old_passwd
            )
    except WrongCredentialsError as e: 
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=400, detail="No se ha podido cambiar la contraseña.")







