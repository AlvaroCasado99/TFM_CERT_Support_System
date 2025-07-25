import streamlit as st

# Panel de lectura de documentos
def smishing_view():
    st.title("📄 Lector de Documentos")
    uploaded_file = st.file_uploader("Sube un documento")
    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
        st.text_area("Contenido del documento", content, height=300)
    if st.button("Volver al Dashboard"):
        st.session_state.page = 'dashboard'
