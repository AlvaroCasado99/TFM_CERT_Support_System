from typing import Dict, Any, Tuple
from web.services.api_client import api_client

"""
    Lanza una petición síncrona a la API para registrar un nuevo usuario
"""
def register_new_user(user: dict) -> bool:
    return api_client.request_data(
        endpoint="user/register", 
        data=user
    )

"""
    Lanza una petición síncrona a la API para cambiar la contraseña de un usuario
"""
def change_user_passwd(username: str, old_passwd: str, new_passwd: str) -> bool:
    return api_client.request_data(
            endpoint="user/change_pass",
            data={
                "username": username,
                "old_passwd": old_passwd,
                "new_passwd": new_passwd
            }
        )

