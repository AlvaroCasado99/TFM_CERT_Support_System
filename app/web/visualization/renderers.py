import io
from typing import Dict, Any, Tuple
from weasyprint import HTML
from web.resources.templates import smishing_report_template
from web.utils.datetime_utils import get_current_timestamp

# Devuelve un reporte listo para mustrar en la web
def pdf_renderer(html: str):
    pdf_io = io.BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    return pdf_io.getvalue()
