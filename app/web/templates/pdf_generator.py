""" Aquí se crea el código HTML de los reportes incrustando los datos en las plantillas hasta tener un informe listo"""

from typing import Dict, Any, Tuple
import web.templates.html_templates as templates
from web.utils.datetime_utils import get_current_timestamp
from web.visualization.renderers import pdf_renderer

# Genera el reporte de smishing en html con los datos que le han pasado
def smishing_report_generator(data: Dict[str, Any] | list, user: Dict[str, Any]):

    # Función local que rellena el cuerpo del reporte
    def format_body(data: Dict[str, Any], user: Dict[str, Any], body: str, timestamp: str) -> str:
        page = body.replace("{{date}}", timestamp)
        page = page.replace("{{name}}", user['name'])
        page = page.replace("{{surname}}", user['surname'])
        page = page.replace("{{message}}", data['msg'])
        page = page.replace("{{flavour}}", data['flavour'])
        page = page.replace("{{campaign}}", data['campaign'])
        page = page.replace("{{orgs}}", data['entity'] if data['entity'] else "-")
        page = page.replace("{{email}}", data['mail'] if data['mail'] else "-")
        page = page.replace("{{url}}", data['url'] if data['url'] else "-")
        page = page.replace("{{active}}", "Sí" if data['html'] else "No")
        return page
    
    # Variables
    timestamp = get_current_timestamp() # Obtiene el instante en el que se elabora el reporte
    html = ""

    # Contruir el reporte en HTML
    if isinstance(data, list):
        pages = [format_body(d, user, templates.SMISHING_REPORT_BODY, timestamp) for d in data]
        joined_pages = templates.PAGE_BREAK.join(pages) # Juntar todos los reportes por un salto de página
        html = templates.SMISHING_REPORT_TEMPLATE.replace("{{body}}", joined_pages)
    else:
        page = format_body(data, user, templates.SMISHING_REPORT_BODY, timestamp)
        html = templates.SMISHING_REPORT_TEMPLATE.replace("{{body}}", page)

    # Renderizar y devolver el resultado
    return pdf_renderer(html=html)

