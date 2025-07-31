import httpx
import logging
import base64

import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from io import BytesIO
from matplotlib.figure import Figure

logger = logging.getLogger("frontend")
PASTEL_COLORS = [
    '#FFB3BA',  # Rosa suave
    '#BAFFC9',  # Verde menta
    '#E1BAFF',  # Lavanda
    '#FFCBA4',  # Naranja pastel
    '#BAE1FF',  # Azul cielo
    '#E6FFB3',  # Verde amarillento
    '#FFB3E6',  # Magenta pastel
    '#B3E5D1',  # Aqua suave
    '#D4A4FF',  # Violeta suave
    '#FFFFBA',  # Amarillo pastel
    '#FFBAE1',  # Rosa chicle
    '#C9FFBA',  # Verde lima suave
    '#DDA0DD',  # Ciruela pastel
    '#FFE4BA',  # Crema
    '#A4E4FF',  # Azul bebé
    '#D1FFE6',  # Verde agua
    '#FFDFBA',  # Melocotón
    '#FFEAA7',  # Amarillo mantequilla
    '#FFD1DC',  # Rosa bebé
    '#F0E68C'   # Khaki pastel
]


CHART_COLORS = [
    '#E74C3C',  # Rojo vibrante
    '#2ECC71',  # Verde esmeralda
    '#3498DB',  # Azul brillante
    '#F39C12',  # Naranja dorado
    '#9B59B6',  # Púrpura
    '#1ABC9C',  # Turquesa
    '#E67E22',  # Naranja oscuro
    '#34495E',  # Azul gris oscuro
    '#F1C40F',  # Amarillo brillante
    '#8E44AD',  # Violeta
    '#16A085',  # Verde azulado
    '#D35400',  # Naranja quemado
    '#2980B9',  # Azul océano
    '#27AE60',  # Verde bosque
    '#C0392B',  # Rojo oscuro
    '#F7DC6F',  # Amarillo suave
    '#BB8FCE',  # Lavanda medio
    '#52C4B0',  # Menta
    '#EC7063',  # Rosa coral
    '#5DADE2'   # Azul cielo
]


"""
    Convierte una imagen a base64 y crea unt tag html con la imagen incrustada
"""
def _get_figure_html_tag(fig) -> str:
    # Creo un buffer de bytes donde escribir la imagen
    buffer = BytesIO() 
    fig.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    img_bytes = buffer.read()

    # Convertir los bytes a base64
    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    tag = f"""<img src="data:image/png;base64,{img_base64}"/>"""
    return tag

"""
    Peticiones a los endpoints de gráficos
"""
def _request_graph_data(url: str, data: dict) -> dict:
    try:
        # Lanzar peticion a la API
        with httpx.Client() as client:
            res = httpx.post(url, json=data, timeout=10)
            res.raise_for_status()
            return {"ok": True,  "data": res.json()}

    except httpx.RequestError as e:
        print(f"Request Error {e}")
        return {"ok": False, "error": "Error de conexión. Inténtelo más tarde."}

    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code
        print(f"He recogido este error: {status_code} -> {e}")
        if status_code >= 500:
            return {"ok": False, "error": "Error del servidor. Inténtelo más tarde."}
        else:
            return {"ok": False, "error": f"Ha ocurrido un error inesperado ({status_code})."}

    except Exception as e:
        return {"ok": False, "error": f"Ha ocurrido un error inesperado ({e})."}



def _no_data_plot(title="Gráfico", message="No hay datos disponibles", 
                       subtitle=None, figsize=(8, 6), text_color='#666666') -> Figure:
    """
    Crea un gráfico que muestra un mensaje de 'no hay datos'
    
    Args:
        title: Título del gráfico
        message: Mensaje principal
        subtitle: Mensaje secundario opcional
        figsize: Tamaño de la figura
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Ocultar ejes y ticks
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Mensaje principal
    ax.text(0.5, 0.6, message, 
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes,
            fontsize=16,
            color=text_color,
            weight='bold')
    
    # Mensaje secundario si se proporciona
    if subtitle:
        ax.text(0.5, 0.4, subtitle, 
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transAxes,
                fontsize=12,
                color='#999999',
                style='italic')
    
    # Título
    ax.set_title(title, fontsize=14, pad=20)
    
    plt.tight_layout()
    return fig

"""
    Este gráfico muestra el volumen de reportes en un plazo dado.
    Las barras deben mostrar la proporción de cada tipo de mensaje.
"""
def report_activity_bar_graph(period: dict) -> tuple[Figure, str]:
    pass


"""
    Este gráfico muestra las principales organizaciones suplantadas en un plazo dado.
"""
def organizations_bar_graph(period: dict) -> tuple[Figure, str]:
    fig = Figure()
    tag = ""

    title = "Organizaciones más suplantadas"
    legend_title = "Categorias"
    figsize = (8, 6)
    height = 0.5

    # Peticion al endpoint de este tipo de gráfico
    result = _request_graph_data(
            url="http://localhost:8000/graph/categories_organizations", 
            data={
                'start': period['start'].isoformat(), 
                'end': period['end'].isoformat()
            }
        )

    # Comprobar el contenido de la peticion
    if result['ok']:

        # Comprobar que hay datos:
        if result['data'] == None:
            fig = _no_data_plot(title=title, figsize=figsize)
            tag = _get_figure_html_tag(fig)
            return fig, tag 
        
        # Datos
        print(result['data'])
        labels = result['data']['organizations']
        values = result['data']['values']
        categories = result['data']['categories']

        # Crear figura con tamaño (anchura, altura) en pulgadas
        fig, ax = plt.subplots(figsize=figsize)
        left = np.zeros(len(labels))

        color_idx = 0
        for category, value in values.items():
            color = CHART_COLORS[color_idx % len(CHART_COLORS)]
            p = ax.barh(
                    labels, 
                    value, 
                    height, 
                    label=category,
                    color=color,
                    left=left
                )
            left += value
            color_idx += 1

        # Leyenda personalizada
        ax.legend(
            categories,
            title=legend_title,
            loc="lower right",
        )

        # Estilo del gráfico
        ax.set_title(title)
        ax.set_xlabel('Cantidad de Reportes')
        ax.set_xlabel('Organizaciones')
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        plt.tight_layout()

    else:
        fig = _no_data_plot(title=title, message="A ocurrido un error con el gráfico.", 
                            text_color="red", figsize=figsize)
        st.error(result['error'])
    
    # Convertir la figura en una tag incrustable
    tag = _get_figure_html_tag(fig)

    return fig, tag


"""
    Este gráfico muestra las categorías más comunes de mensajes en un plazo dado.
"""
def smishing_categories_bar_graph(period: dict, interval: str) -> tuple[Figure, str]:
    fig = Figure()
    tag = ""

    title = "Volumen de reportes categorizados"
    legend_title = "Categorias"
    figsize = (6, 6)
    width = 0.5

    # Peticion al endpoint de este tipo de gráfico
    result = _request_graph_data(
            url="http://localhost:8000/graph/stack_bar_time_categories", 
            data={
                'start': period['start'].isoformat(), 
                'end': period['end'].isoformat(),
                'interval': interval
            }
        )

    # Comprobar el contenido de la peticion
    if result['ok']:

        # Comprobar que hay datos:
        if result['data'] == None:
            fig = _no_data_plot(title=title, figsize=figsize)
            tag = _get_figure_html_tag(fig)
            return fig, tag 
        
        # Datos
        labels = result['data']['timestamps']
        values = result['data']['values']
        categories = result['data']['categories']

        # Crear figura con tamaño (anchura, altura) en pulgadas
        fig, ax = plt.subplots(figsize=figsize)
        bottom = np.zeros(len(labels))

        color_idx = 0
        for category, value in values.items():
            color = CHART_COLORS[color_idx % len(CHART_COLORS)]
            p = ax.bar(
                    labels, 
                    value, 
                    width, 
                    label=category,
                    color=color,
                    bottom=bottom
                )
            bottom += value
            color_idx += 1

        # Leyenda personalizada
        ax.legend(
            categories,
            title=legend_title,
            loc="upper right",
            #bbox_to_anchor=(1, 0.5)
        )

        # Estilo del gráfico
        ax.set_title(title)
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        plt.tight_layout()

    else:
        fig = _no_data_plot(title=title, message="A ocurrido un error con el gráfico.", 
                            text_color="red", figsize=figsize)
        st.error(result['error'])
    
    # Convertir la figura en una tag incrustable
    tag = _get_figure_html_tag(fig)

    return fig, tag

"""
    Este gráfico muestra una nube de palabras con los términos más comunes en un plazo dado.
"""
def word_cloud(period: dict):
    pass

"""
    Este gráfico muestra una pie chart con las proporciones de tipos de mensajes
"""
def smishing_categories_pie_chart(period: dict) -> tuple[Figure, str]:
    fig = Figure()
    tag = ""

    title = "Proporción de Categorías de Smishing"
    legend_title = "Categorias"
    figsize = (6, 6)

    # Peticion al endpoint de este tipo de gráfico
    result = _request_graph_data(
            url="http://localhost:8000/graph/msg_categories", 
            data={'start': period['start'].isoformat(), 'end': period['end'].isoformat()}
        )

    # Comprobar el contenido de la peticion
    if result['ok']:

        # Comprobar que hay datos:
        if result['data'] == None:
            fig = _no_data_plot(title=title, figsize=figsize)
            tag = _get_figure_html_tag(fig)
            return fig, tag 
        
        # Datos
        labels = result['data']['labels']
        values = result['data']['counts']

        # Crear figura con tamaño (anchura, altura) en pulgadas
        fig, ax = plt.subplots(figsize=figsize)

        # Pie chart
        wedges, texts, autotexts = ax.pie(
            values,
            labels=None,  # Las etiquetas las mandamos a la leyenda
            colors=PASTEL_COLORS,
            autopct="%1.1f%%",  # Mostrar porcentajes
            startangle=90,      # Rotar inicio del gráfico
            pctdistance=0.7     # Distancia del % al centro
        )

        # Leyenda personalizada
        ax.legend(
            wedges,
            labels,
            title=legend_title,
            loc="center left",
            bbox_to_anchor=(1, 0.5)
        )

        # Estilo del gráfico
        ax.set_title(title)
        plt.tight_layout()

    else:
        fig = _no_data_plot(title=title, message="A ocurrido un error con el gráfico.", 
                            text_color="red", figsize=figsize)
        st.error(result['error'])
    
    # Convertir la figura en una tag incrustable
    tag = _get_figure_html_tag(fig)

    return fig, tag
