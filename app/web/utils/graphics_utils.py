import base64

from io import BytesIO
from matplotlib.figure import Figure

"""
    Convierte una imagen a base64 y crea unt tag html con la imagen incrustada
"""
def get_figure_html_tag(fig: Figure) -> str:
    # Creo un buffer de bytes donde escribir la imagen
    buffer = BytesIO() 
    fig.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    img_bytes = buffer.read()

    # Convertir los bytes a base64
    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    tag = f"""<img src="data:image/png;base64,{img_base64}"/>"""
    return tag
