import matplotlib.pyplot as plt
import numpy as np

from typing import Dict, Tuple, Any, Optional
from decimal import Decimal
from matplotlib.figure import Figure
from wordcloud import WordCloud

from web.utils.constants import PASTEL_COLORS, CHART_COLORS

def create_no_data_chart(
    title: str = "Gráfico",
    message: str = "No hay datos disponibles",
    subtitle: str = None,
    figsize: Tuple[int, int] = (8, 6),
    text_color: str = '#666666'
) -> Figure:

    fig, ax = plt.subplots(figsize=figsize)

    # Ocultar ejes y ticks
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Mensaje principal
    ax.text(0.5, 0.6, 
            message, 
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes,
            fontsize=16,
            color=text_color,
            weight='bold'
        )

    # Mensaje secundario si se proporciona
    if subtitle:
        ax.text(0.5, 0.4, 
                subtitle, 
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transAxes,
                fontsize=12,
                color=text_color,
                style='italic'
            )

    # Otros parametros 
    ax.set_title(title, fontsize=14, pad=20)
    plt.tight_layout()

    return fig



def create_word_cloud_chart(
    text: str, 
    title: str = "Wordclouds de Smishing",
    figsize: Tuple[int, int] = (10, 6),
    height: int = 400,
    width: int = 800,
    background: str = 'white'
) -> Figure:

    # Wordcloud
    wc = WordCloud(width=width, height=height, background_color=background).generate(text)

    # Generar figura
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(title)
    plt.tight_layout()

    return fig




def create_pie_chart(
    labels: list,
    values: list,
    title: str = "Proporción de Categorías de Smishing",
    legend_title: str = "Categorias",
    figsize: Tuple[int, int] = (10, 6)
) -> Figure:
    
    # Crear figura con tamaño (anchura, altura) en pulgadas
    fig, ax = plt.subplots(figsize=figsize)

    # Pie chart
    wedges, texts, autotexts = ax.pie(
        values,
        labels=None,  
        colors=PASTEL_COLORS,
        autopct="%1.1f%%",  
        startangle=90,      
        pctdistance=0.7     
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

    return fig


def create_stacked_bar_chart(
        labels: list,
        values: Dict[str, list],
        categories: list,
        orientation: str = 'vertical',
        figsize: Tuple[int, int] = (10, 6),
        title: str = "Gráfico",
        legend_title: str = "Leyenda",
        bar_size: Decimal | int = 0.5

    ) -> Figure:
    
    fig, ax = plt.subplots(figsize=figsize)

    if orientation ==  'horizontal':
        left = np.zeros(len(labels))
        color_idx = 0

        for category, value in values.items():
            color = CHART_COLORS[color_idx % len(CHART_COLORS)]
            p = ax.barh(labels, value, bar_size, 
                    label=category, color=color, left=left)
            left += value
            color_idx += 1

        # Estilos para orientación horizontal
        ax.set_title(title)
        ax.set_xlabel('Cantidad de Reportes')
        ax.set_ylabel('Organizaciones')
        ax.legend(categories, title=legend_title, loc="lower right")
        plt.setp(ax.get_yticklabels(), rotation=45, ha='right')
    else:
        # Crear figura con tamaño (anchura, altura) en pulgadas
        fig, ax = plt.subplots(figsize=figsize)
        bottom = np.zeros(len(labels))

        color_idx = 0
        for category, value in values.items():
            color = CHART_COLORS[color_idx % len(CHART_COLORS)]
            p = ax.bar(labels, value, bar_size, 
                       label=category, color=color, bottom=bottom)
            bottom += value
            color_idx += 1

        # Leyenda personalizada
        ax.set_title(title)
        ax.set_ylabel('Cantidad de Reportes')
        ax.set_xlabel('Tiempo')
        ax.legend(categories, title=legend_title, loc="upper right")
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    plt.tight_layout()

    return fig



