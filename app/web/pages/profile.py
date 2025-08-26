import logging
import streamlit as st

from web.services.user_services import change_user_passwd

logger = logging.getLogger("frontend")

def profile_view():
    st.title("👤 Perfil de Usuario")
    st.markdown("---")

    # --- Contenedor de información del usuario ---
    with st.container():
        user = st.session_state.user
        st.subheader("Información del Usuario")
        st.text(f"Nombre: {user['name']}")
        st.text(f"Apellido: {user['surname']}")
        st.text(f"Usuario: {user['username']}")
        st.text(f"Email: {user['email']}")
        st.text(f"Teléfono: {user['phone'] if user['phone'] else 'No registrado'}")
        st.text(f"Rol: {user['rol']}")

    st.markdown("---")

    # --- Contenedor para cambiar contraseña ---
    with st.container():
        st.subheader("Cambiar Contraseña")

        user = st.session_state.user

        with st.form("password_form", clear_on_submit=True):
            old_password = st.text_input("Contraseña actual", type="password")
            new_password = st.text_input("Nueva contraseña", type="password")
            confirm_password = st.text_input("Confirmar nueva contraseña", type="password")

            button = st.form_submit_button("Actualizar contraseña")

            if button:
                if not old_password or not new_password or not confirm_password:
                    st.error("Todos los campos son obligatorios.")
                elif new_password != confirm_password:
                    st.error("Las contraseñas nuevas no coinciden.")
                elif new_password == old_password:
                    st.error("No se puede usar la misma contraseña.")
                else:
                    result = change_user_passwd(
                        username=user['username'],
                        old_passwd=old_password,
                        new_passwd=new_password
                    )
                    
                    if result:
                        st.success("✅ Contraseña actualizada correctamente.")
