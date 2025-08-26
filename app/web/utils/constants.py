"""
    Es este archivo se encuetran todas las constantes usadas en el fronted Streamlit
"""

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

FOOTER_CSS = """
<style>
/* Hace que el contenedor ocupe la altura de la ventana y el footer quede al final */
main .block-container{
  min-height: calc(100vh - 80px);
  display: flex;
  flex-direction: column;
}
.app-footer{
  margin-top: auto;               /* empuja el footer al fondo */
  border-top: 1px solid #EEE;
  padding: 12px 0 24px 0;
  text-align: center;
  color: #666;
  font-size: 0.9rem;
}
.app-footer .sep{ margin: 0 8px; color: #AAA; }
</style>
"""

PRIVACY_POLICY = """El presente sistema (aplicación web y bot de Telegram) tiene como finalidad detectar y analizar mensajes sospechosos de smishing con fines de concienciación y ciberseguridad.

Responsable del tratamiento: Álvaro Casado Miguelez — Contacto: [acasam@antismish.es].

Datos tratados:
- En la aplicación web: credenciales de acceso (nombre de usuario, contraseña cifrada, correo electrónico, rol de usuario) y registros de actividad.
- En el bot: mensajes de texto enviados por el usuario, que pueden incluir direcciones URL o direcciones de correo electrónico. No se emplean datos con fines publicitarios.

Finalidad del tratamiento: ofrecer al usuario un análisis del mensaje y elaborar estadísticas agregadas sobre intentos de fraude.

Base jurídica: interés legítimo en la prevención del fraude y la seguridad (art. 6.1.f RGPD).

Conservación: los datos se conservarán el tiempo estrictamente necesario para el análisis y la generación de estadísticas, eliminándose o anonimizándose posteriormente.

Destinatarios: no se cederán datos a terceros salvo obligación legal.

Derechos de los usuarios: puede ejercer sus derechos de acceso, rectificación, supresión, limitación, oposición y portabilidad enviando una solicitud a [legal@antismish.es]. También puede retirar su consentimiento cuando proceda y presentar una reclamación ante la AEPD.

Medidas de seguridad: las contraseñas se almacenan mediante algoritmos de hash con salting; las comunicaciones de la aplicación web están cifradas con TLS/SSL; el acceso a los datos se controla mediante roles.
"""

LEGAL_DISCLAIMER = """El presente servicio (aplicación web y bot de Telegram) es una herramienta de carácter experimental y académico diseñada para el análisis de mensajes sospechosos de smishing.

El acceso y uso de la herramienta implica la aceptación de los siguientes términos:

El sistema no garantiza la detección total de fraudes y no sustituye la verificación directa con la entidad legítima.

El usuario se compromete a no introducir datos personales innecesarios ni confidenciales en los mensajes remitidos.

El servicio no tiene finalidad comercial y se ofrece únicamente con fines de investigación y concienciación en ciberseguridad.

Para cualquier consulta o ejercicio de derechos relacionados con el tratamiento de datos, puede dirigirse a legal@antismish.es.
"""

INTERVAL_CODE = {
        "Hoy":'H',
        "7 días":'D',
        "Mes":'D',
        "Año": 'W',
        "Todo": 'M'
}

API_URL="http://api:8000"

FILE_MESSAGE_COLUMN="TEXT"

USER_ROL="user"
ADMIN_ROL="admin"
ROOT_ROL="root"
