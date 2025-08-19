import asyncio
import httpx
import logging
import streamlit as st

from web.utils.form_utils import is_valid_email
from web.services.user_services import register_new_user

logger = logging.getLogger("frontend")


"""
    Formulario para nuevos usuarios
"""
def _load_new_user_form():
    st.title("Nuevo usuario")
    
    # Campos de entrada
    name = st.text_input("Nombre")
    surname = st.text_input("Apellido")
    username = st.text_input("Nombre de usuario")
    email = st.text_input("Email")
    phone = st.text_input("Teléfono (opcional)")
    rol = st.selectbox("Rol", ["user", "admin"])

    # Botón de envío
    if st.button("Enviar"):

        # Validación
        if not name or not surname or not username or not email:
            st.error("Por favor, completa todos los campos obligatorios.")
        elif not is_valid_email(email):
            st.error("El email no tiene un formato válido.")

        result = register_new_user({
                "name": name,
                "surname": surname,
                "username": username,
                "email": email,
                "phone": phone if phone else None,
                "rol": rol
            })

        if result:
            st.success(f"✅ Usuario <{username}> creado correctamente")

        # Resetear inputs
        st.session_state.name = ""
        st.session_state.surname = ""
        st.session_state.username = ""
        st.session_state.email = ""
        st.session_state.phone = ""
        st.session_state.rol = ""


"""
    Formulario para eliminar un usuario
"""
def _delete_user_form():
    pass
        


"""
    Tiene la vista para administrar usuarios
"""
def hr_view():
    with st.container():
        _load_new_user_form()
