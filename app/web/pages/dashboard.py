import streamlit as st

import web.visualization.chart_generator as cg
from web.utils.datetime_utils import obtener_rango_fechas
from web.utils.constants import INTERVAL_CODE

# Panel de gráficos
def dashboard_view():
    st.title("📊 Panel de Gráficos")
    col1, col2 = st.columns((1.5, 5), gap="medium")

    with col1:
        # Seleccionar el tipo de gráfico
        graph = st.selectbox("Tipo de Gráfico", ["Tarta", "Barras", "Organizaciones", "Palabras"])
        # Seleccionar el periodo
        period = st.selectbox("Periodo", ["Hoy", "7 días", "Mes", "Año", "Todo"])

    with col2:
        inicio, fin = obtener_rango_fechas(period)
        if graph == "Tarta":
            fig, tag = cg.smishing_categories_pie_chart(period={'start': inicio, "end": fin})
            st.pyplot(fig)
        elif graph == "Barras":
            fig, tag = cg.smishing_categories_bar_graph(
                    period={'start': inicio, "end": fin}, 
                    interval = INTERVAL_CODE[period]
                )
            st.pyplot(fig)
        elif graph == "Organizaciones":
            fig, tag = cg.organizations_categories_bar_graph(
                    period={'start': inicio, "end": fin} 
                )
            st.pyplot(fig)
        elif graph == "Palabras":
            fig, tag = cg.smishing_word_cloud(
                    period={'start': inicio, "end": fin}
                )
            st.pyplot(fig)
