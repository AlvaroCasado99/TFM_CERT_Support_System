import bcrypt

from fastapi import APIRouter, HTTPException, status
from app.models.user import User, UserRequest

# Router
router = APIRouter()


# Endpoint de prueba para este router
@router.get("/test")
def get_analysis_test():
    return {
            "message": "Router /user funciona!"
            }

# Endpoint para autenticar usuarios
@router.post("/login")
async def user_login(req: UserRequest):
    user = await User.find_one({"username": req.username})

    # Comprobar que existe el usuario
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials", headers={"WWW-Authenticate": "Bearer"})
        
    # Comprobar que la contraseña es correcta
    match = bcrypt.checkpw(req.password.encode('utf-8'), user.password.encode('utf-8'))
    if not match:
        raise HTTPException(status_code=401, detail="Invalid Credentials", headers={"WWW-Authenticate": "Bearer"})
    
    # Crear nuevo token

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


#@router.post("/register")
#async def user_register():
#    hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10)).decode("utf-8")

