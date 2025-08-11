import httpx
import logging

import streamlit as st

from web.utils.graphics_utils import get_figure_html_tag
import web.services.chart_data_service as cds
import web.visualization.charts as charts

from matplotlib.figure import Figure
from typing import Dict, Tuple, Any

logger = logging.getLogger("frontend")


"""
    Este gráfico muestra las principales organizaciones suplantadas en un plazo dado.
"""
def organizations_categories_bar_graph(period: Dict[str, Any]) -> Tuple[Figure, str]:

    title = "Gráfico con las organizaciones más suplantadas",

    # Peticion al endpoint de este tipo de gráfico
    result = cds.get_entities_categories_data(period=period)

    # Comprobar el contenido de la peticion
    if result['ok']:

        # Comprobar que hay datos:
        if result['data'] == None:
            fig = charts.create_no_data_chart(title=title)
            tag = get_figure_html_tag(fig)
            return fig, tag 
    
        # Crear figura
        fig = charts.create_stacked_bar_chart(
            labels = result['data']['organizations'],
            values = result['data']['values'],
            categories = result['data']['categories'],
            orientation = 'horizontal',
            title = title,
            legend_title = "Categorias"
        )
    else:
        fig = charts.create_no_data_chart(
            title=title, 
            message="A ocurrido un error con el gráfico.", 
            text_color="red"
        )
        st.error(result['error'])

    # Convertir la figura en una tag incrustable
    tag = get_figure_html_tag(fig)

    return fig, tag


"""
    Este gráfico muestra las categorías más comunes de mensajes en un plazo dado.
"""
def smishing_categories_bar_graph(period: Dict[str, Any], interval: str) -> Tuple[Figure, str]:
    title = "Volumen de reportes categorizados"

    # Peticion al endpoint de este tipo de gráfico
    result = cds.get_categories_time_data(period=period, interval=interval)

    # Comprobar el contenido de la peticion
    if result['ok']:

        # Comprobar que hay datos:
        if result['data'] == None:
            fig = charts.create_no_data_chart(title=title)
            tag = get_figure_html_tag(fig)
            return fig, tag 
    
        # Crear figura con tamaño (anchura, altura) en pulgadas
        fig = charts.create_stacked_bar_chart(
            labels = result['data']['timestamps'],
            values = result['data']['values'],
            categories = result['data']['categories'],
            orientation = 'vertical',
            title = title,
            legend_title = "Categorias"
        )

    else:
        fig = charts.create_no_data_chart(
                title=title, 
                message="A ocurrido un error con el gráfico.", 
                text_color="red"
            )
        st.error(result['error'])

    # Convertir la figura en una tag incrustable
    tag = get_figure_html_tag(fig)

    return fig, tag



"""
    Este gráfico muestra una nube de palabras con los términos más comunes en un plazo dado.
"""
def smishing_word_cloud(period: Dict[str, Any]) -> Tuple[Figure, str]:
    title = "Wordclouds de Smishing"

    # Peticion al endpoint de este tipo de gráfico
    result = cds.get_smishing_text_data(period=period)

    # Comprobar el contenido de la peticion
    if result['ok']:

        # Comprobar que hay datos:
        if result['data'] == None:
            fig = charts.create_no_data_chart(title=title)
            tag = get_figure_html_tag(fig)
            return fig, tag 
    
        # Crear figura
        fig = charts.create_word_cloud_chart(
                text=result['data']['joined'], 
                title=title
            )

    else:
        fig = charts.create_no_data_chart(
                title=title, 
                message="A ocurrido un error con el gráfico.", 
                text_color="red"
            )
        st.error(result['error'])

    # Convertir la figura en una tag incrustable
    tag = get_figure_html_tag(fig)

    return fig, tag




"""
    Este gráfico muestra una pie chart con las proporciones de tipos de mensajes
"""
def smishing_categories_pie_chart(period: Dict[str, Any]) -> Tuple[Figure, str]:
    title = "Proporción de Categorías de Smishing"

    # Peticion al endpoint de este tipo de gráfico
    result = cds.get_categories_data(period=period)

    # Comprobar el contenido de la peticion
    if result['ok']:

        # Comprobar que hay datos:
        if result['data'] == None:
            fig = charts.create_no_data_chart(title=title)
            tag = get_figure_html_tag(fig)
            return fig, tag 
    
        # Crear figura
        fig = charts.create_pie_chart(
                labels = result['data']['labels'],
                values = result['data']['counts'],
                title = title
            )
    
    else:
        fig = charts.create_no_data_chart(
                title=title, 
                message="A ocurrido un error con el gráfico.", 
                text_color="red"
            )
        st.error(result['error'])

    # Convertir la figura en una tag incrustable
    tag = get_figure_html_tag(fig)

    return fig, tag
