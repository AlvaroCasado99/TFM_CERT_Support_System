import streamlit as st

from logger_config.setup_logger import setup_logger

from pages.login import login_view, logout
from pages.dashboard import dashboard_view
from pages.smishing import smishing_view

logger = setup_logger("frontend", "frontend.log", "./logs")
logger.info("Arrancando streamlit.")

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
    dashboard_page = st.Page(dashboard_view, title="Dashboard", icon=":material/dashboard:", default=True)
    smishing_page = st.Page(smishing_view, title="Smishing Report", icon=":material/bug_report:")

    # Definir la barra de navegación
    if st.session_state.logged_in:
        pg = st.navigation(
            {
                "Account": [logout_page],
                "Reports": [dashboard_page, smishing_page]
            }
        )
    else:
        pg = st.navigation([login_page])
        
    pg.run()

if __name__ == "__main__":
    main()
