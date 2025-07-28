import httpx
import io
import logging
import streamlit as st
import pandas as pd

from weasyprint import HTML

from web.resources.templates import smishing_report_template

# Iniciar el logger
logger = logging.getLogger("frontend")

# Devuelve un reporte listo para mustrar en la web
def generate_pdf(data):
    logger.info("Voy a generar un reporte con los datos")
    html = smishing_report_template(data, st.session_state.user)
    pdf_io = io.BytesIO()
    HTML(string=html).write_pdf(pdf_io)

    return pdf_io.getvalue()

# Procesa el contenido de un dataframe
def process_messages(df):
    logger.info("Voy a procesar los mensajes del archivo")
    try:
        messages = df["TEXT"].to_list()
        with httpx.Client() as client:
            res = httpx.post("http://localhost:8000/analyse/text/advanced", json={"msg":messages}, timeout=120)
            res.raise_for_status()
            return {"ok": True,  "data": res.json()}
    except httpx.RequestError as e:
        print(f"Request Error {e}")
        return {"ok": False, "error": "Error de conexión. Inténtelo más tarde."}
    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code
        print(f"He recogido este error: {status_code}")
        if status_code >= 500:
            return {"ok": False, "error": "Error del servidor. Inténtelo más tarde."}
        else:
            return {"ok": False, "error": f"Ha ocurrido un error inesperado ({status_code})."}
    except KeyError:
        return {"ok": False, "error": "La columna con los mensajes debe llamarse TEXT."}
    except Exception as e:
        return {"ok": False, "error": f"Ha ocurrido un error inesperado ({e})."}


# Panel de lectura de documentos
def smishing_view():
    st.title("📄 Lector de Documentos")
    uploaded_file = st.file_uploader("Sube un archivo CSV o XLSX", type=["csv", "xlsx"])
    if uploaded_file:
        logger.info("Se subión un archivo para analizar mensajes.")
        
        # Leer archivo
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)

        # Esperar a que el usuario envie el contenido
        if st.button("Procesar"):
            result = process_messages(df)
            if result['ok']:
                data = result['data']
                
                # Print report
                st.download_button(
                    label="📄 Descargar PDF",
                    data=generate_pdf(data),
                    file_name="reporte.pdf",
                    mime="application/pdf"
                )

            else:
                st.error(result['error'])
            

            # Mostrar contenido
            st.text_area("Contenido del documento", "En proceso...", height=300)
