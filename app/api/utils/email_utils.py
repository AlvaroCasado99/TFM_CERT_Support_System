import smtplib
from email.message import EmailMessage

from exceptions.email_exceptions import SMTPError

"""
    Permite enviar un correo
"""
def send_email(
        src: str, 
        dst: str, 
        topic: str, 
        body: str, 
        password_smtp: str, 
        smtp_server="smtp.gmail.com", 
        smtp_port=587
    ):
   
    msg = EmailMessage()
    msg["From"] = src
    msg["To"] = dst
    msg["Subject"] = topic
    msg.set_content(body)

    try:
        # Conexión segura con el servidor SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(src, password_smtp)
            server.send_message(msg)
        print("Correo enviado con éxito")
    except Exception as e:
        raise SMTPError(f"Error al enviar correo: {e}")
