import streamlit as st

from logger_config.setup_logger import setup_logger

from pages.login import login_view, logout
from pages.dashboard import dashboard_view
from pages.smishing import smishing_view
from pages.hr import hr_view
from pages.profile import profile_view
from pages.legal import privacy_view, legal_disclaimer_view
from utils.constants import USER_ROL, ADMIN_ROL, ROOT_ROL

logger = setup_logger("frontend", "frontend.log", "./logs")
logger.info("Arrancando streamlit.")




# Función principal
def main():
    # Inicializar varibles de sesion
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user' not in st.session_state:
        st.session_state.user = None

    # Inicializar las páginas (Vistas de la aplicacion)
    login_page = st.Page(login_view, title="Log in", icon=":material/login:")
    logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
    profile_page = st.Page(profile_view, title="Profile", icon=":material/account_circle:")
    hr_page = st.Page(hr_view, title="Human Resources", icon=":material/group:")
    dashboard_page = st.Page(dashboard_view, title="Dashboard", icon=":material/dashboard:", default=True)
    smishing_page = st.Page(smishing_view, title="Report", icon=":material/bug_report:")
    privacy_page = st.Page(privacy_view, title="Privacy", icon=":material/privacy_tip:")
    legal_note_page = st.Page(legal_disclaimer_view, title="Legal Note", icon=":material/balance:")

    # Definir la barra de navegación
    if st.session_state.logged_in:
        navs = {
            "Account": [logout_page, profile_page],
            "Reports": [dashboard_page, smishing_page],
            "Legal": [privacy_page, legal_note_page]
        }

        # Añadir vistas exclusivas de usuario administrador
        if st.session_state.user['rol'] in [ADMIN_ROL, ROOT_ROL]:
            navs['Administration'] = [hr_page]
        
        # Crear el navegador
        pg = st.navigation(navs)

    else:
        pg = st.navigation([login_page])
        
    pg.run()

if __name__ == "__main__":
    main()
