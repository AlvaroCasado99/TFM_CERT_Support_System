import streamlit as st

from datetime import datetime, timedelta
from web.resources import graphics as gp

INTERVAL_CODE = {
        "Hoy":'H',
        "7 días":'D',
        "Mes":'D',
        "Año": 'W',
        "Todo": 'M'
    }

# Devuleve un rango de fechas segun las opciones disponibles
def obtener_rango_fechas(rango: str) -> tuple[datetime, datetime]:
    ahora = datetime.now()

    if rango == "Hoy":
        inicio = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
    elif rango == "7 días":
        inicio = (ahora - timedelta(days=6)).replace(hour=0, minute=0, second=0, microsecond=0)
    elif rango == "Mes":
        inicio = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif rango == "Año":
        inicio = ahora.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    elif rango == "Todo":
        inicio = datetime(2000, 1, 1)
    else:
        raise ValueError(f"Rango no reconocido: {rango}")

    fin = ahora
    return inicio, fin

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
            fig, tag = gp.smishing_categories_pie_chart(period={'start': inicio, "end": fin})
            st.pyplot(fig)
        elif graph == "Barras":
            fig, tag = gp.smishing_categories_bar_graph(
                    period={'start': inicio, "end": fin}, 
                    interval = INTERVAL_CODE[period]
                )
            st.pyplot(fig)
        elif graph == "Organizaciones":
            fig, tag = gp.organizations_bar_graph(
                    period={'start': inicio, "end": fin} 
                )
            st.pyplot(fig)
        elif graph == "Palabras":
            fig, tag = gp.smishing_categories_bar_graph(
                    period={'start': inicio, "end": fin}, 
                    interval = INTERVAL_CODE[period]
                )
            st.pyplot(fig)
