import pdfkit
import httpx
import asyncio


"""
"""
def advanced_report_generator(data):
    html_content = """
    <h1>Reporte rápido</h1>
    <p>PDF generado directamente en memoria sin archivos temporales.</p>
    """

    # Generar el PDF directamente como bytes
    pdf_bytes = pdfkit.from_string(html_content, False)

    return Response(content=pdf_bytes, media_type="application/pdf", headers={
        "Content-Disposition": "attachment; filename=report.pdf"
    })
