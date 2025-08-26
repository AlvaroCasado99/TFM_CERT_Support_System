import asyncio
import httpx
import logging
import streamlit as st

from web.utils.constants import PRIVACY_POLICY, LEGAL_DISCLAIMER

logger = logging.getLogger("frontend")

"""
    Vista para mostrar la politica de privacidad de la aplicacion
"""
def privacy_view():
    st.title("Política de privacidad")
    st.write(PRIVACY_POLICY)


"""
    Vista para mostrar el aviso legal
"""
def legal_disclaimer_view():
    st.title("Aviso legal")
    st.write(LEGAL_DISCLAIMER)
