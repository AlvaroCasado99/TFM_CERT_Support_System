import asyncio
import httpx
import logging
import streamlit as st

logger = logging.getLogger("frontend")

"""
    Valida un usuario y actualiza las variables de estado
"""
def login(username, password):
    try:
        with httpx.Client() as client:
            res = client.post(
                    "http://api:8000/user/login", 
                    json={"username": username, "password": password}, 
                    timeout=5.0
                )
            res.raise_for_status()
        
            return {"ok": True,  "data": res.json()}
    except httpx.RequestError as e:
        return {"ok": False, "error": "Error de conexión. Inténtelo más tarde."}
    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code
        if status_code == 401:
            return {"ok": False, "error": "Credenciales Inválidas."}
        elif status_code == 403:
            return {"ok": False, "error": "Acceso denegado."}
        elif status_code >= 500:
            return {"ok": False, "error": "Error del servidor. Inténtelo más tarde."}
        else:
            logger.warning(f"(login) Ha ocurrido un error inesperado ({status_code}).")
            return {"ok": False, "error": f"Ha ocurrido un error inesperado ({status_code})."}



"""
    Cierra la sesion del usuario y cambia las variables
"""
def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.token = None
    st.rerun()



def login_view():
    st.title("🔐 Login")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):
        result = login(username, password)
        if result['ok']:
            st.session_state.logged_in = True
            st.session_state.user = result['data']['user']
            st.session_state.token = result['data']['token']
            st.rerun()
        else:
            st.error(result['error'])
