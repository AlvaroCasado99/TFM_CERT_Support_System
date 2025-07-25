import streamlit as st

# Panel de gráficos
def dashboard_view():
    st.title("📊 Panel de Gráficos")
    st.write("Aquí podrías mostrar gráficos con matplotlib, seaborn o plotly.")
    st.line_chart({'Ventas': [100, 200, 300, 400]})
    if st.button("Ir a Documentos"):
        st.session_state.page = 'documents'
