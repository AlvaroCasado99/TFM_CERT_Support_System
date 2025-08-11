import logging
import streamlit as st
import pandas as pd

import web.services.smishing_data_services as sds
import web.services.smishing_processing_services as sps
from web.templates.pdf_generator import smishing_report_generator

# Iniciar el logger
logger = logging.getLogger("frontend")

# Panel de lectura de documentos
def smishing_view():
    st.title("📄 Reportes de Smishing")
    
    left, center, right = st.columns(3)

    with center:
        seg = st.segmented_control("Elige método de reporte", ["Único", "Múltiple"], default="Único")

    with st.container():
        if seg=="Único":
            text = st.text_area("Introduce aquí el mensaje:", "", height=100)

            # Validar el mensaje
            process_btn = None
            valid = sps.process_single_message(text)

            if not valid['ok']:
                st.error(valid['error'])

            # Procesar contenido
            if st.button('Procesar') and valid['ok']:
                if not text:
                    st.error("Debes introducir un mensaje.")
                else:
                    result = sds.get_analysis_data(text)

                # Comprobar resultados
                if result['ok']:
                    data = result['data']
                    print(data)

                    # Print del reporte
                    st.download_button(
                        label="📄 Descargar PDF",
                        data=smishing_report_generator(data=data, user=st.session_state.user),
                        file_name="reporte.pdf",
                        mime="application/pdf"
                        )

                    with st.expander(f"📨 Análisis mensaje"):
                        st.markdown(f"""
                        **Mensaje:**  
                        ```
                        {data['msg']}
                        ```

                        - **Tipo:** {data['flavour']}
                        - **Entidades:** {data['entity']}
                        - **URL:** {data['url']}
                        - **Campaña:** {data['campaign']}
                        """)

                else:
                    st.error(result['error'])

            
            

    with st.container():
        if seg=="Múltiple":
            uploaded_file = st.file_uploader("Sube un archivo CSV o XLSX", type=["csv", "xlsx"], help="Sube un archivo CSV o XLSX con la columna TEXT conteniendo los mensajes.")
            if uploaded_file:
                logger.info("Se subió un archivo para analizar mensajes.")

                # Llamar al validador
                df = None
                process_btn = None
                valid = sps.process_multiple_messages(uploaded_file)

                if valid['ok']:
                    df = valid['result']

                    # Avisar si se han filtrado mensajes
                    if valid['warn']:
                        st.warning(valid['warn'])

                    # Revisar si quedan mensajes
                    if df.empty:
                        st.error("No hay mensajes dentro del archivo")
                    else:
                        process_btn = st.button('Procesar')
                else:
                    st.error(valid['error'])
        
                # Esperar a que el usuario envie el contenido
                data = None
                if process_btn:
                    messages = df['TEXT'].to_list()
                    result = sds.get_analysis_data(messages)

                    if result['ok']:
                        data = result['data']
                        processed = True
                
                        # Print del reporte
                        st.download_button(
                            label="📄 Descargar PDF",
                            data=smishing_report_generator(data=data, user=st.session_state.user),
                            file_name="reporte.pdf",
                            mime="application/pdf"
                        )

                        for i, msg in enumerate(data):
                            with st.expander(f"📨 Análisis mensaje {i+1}"):
                                st.markdown(f"""
                                **Mensaje:**  
                                ```
                                {msg['msg']}
                                ```

                                - **Tipo:** {msg['flavour']}
                                - **Entidades:** {msg['entity']}
                                - **URL:** {msg['url']}
                                - **Campaña:** {msg['campaign']}
                                """)
                    else:
                        st.error(result['error'])

