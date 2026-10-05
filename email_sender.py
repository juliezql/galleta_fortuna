# email_sender.py
# Este módulo se encarga SOLO de enviar el correo.

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def conectar_y_enviar(servidor, mensaje, remitente, password):
    """
    Intenta enviar primero por el puerto 465 (SSL).
    Si falla la conexión, intenta por el puerto 587 (STARTTLS).
    """
    try:
        # Intento 1: puerto 465 con SSL
        with smtplib.SMTP_SSL(servidor, 465, timeout=15) as conexion:
            conexion.login(remitente, password)
            conexion.send_message(mensaje)
    except smtplib.SMTPAuthenticationError:
        # Si la clave es incorrecta, no tiene sentido probar el otro puerto
        raise
    except (smtplib.SMTPException, OSError):
        # Intento 2: puerto 587 con STARTTLS
        with smtplib.SMTP(servidor, 587, timeout=15) as conexion:
            conexion.starttls()
            conexion.login(remitente, password)
            conexion.send_message(mensaje)


def enviar_frase(destinatario, frase):
    """
    Envía la frase al correo del destinatario.
    Devuelve una tupla: (True/False, mensaje para mostrar al usuario).
    """
    # 1. Leer la configuración desde las variables de entorno (.env)
    remitente = os.getenv("EMAIL_REMITENTE")
    password = os.getenv("EMAIL_PASSWORD")
    servidor = os.getenv("SMTP_SERVER", "smtp.gmail.com")

    if not remitente or not password:
        return False, "Falta configurar EMAIL_REMITENTE y EMAIL_PASSWORD en el archivo .env"

    # Por si la clave de aplicación se copió con espacios
    password = password.replace(" ", "")

    # 2. Armar el correo
    mensaje = EmailMessage()
    mensaje["Subject"] = "Tu galleta de la fortuna 🍪"
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje.set_content(
        "¡Hola!\n\n"
        "Abriste una galleta de la fortuna y esto fue lo que salió:\n\n"
        f"    \"{frase}\"\n\n"
        "Que tengas un gran día. ¡Sigue adelante!\n\n"
        "- Galleta de la Fortuna 🍪"
    )

    # 3. Enviar
    try:
        conectar_y_enviar(servidor, mensaje, remitente, password)
        return True, "¡Correo enviado correctamente! Revisa tu bandeja de entrada."

    except smtplib.SMTPAuthenticationError:
        return False, "Error de autenticación: revisa el correo y la contraseña de aplicación en el .env"
    except smtplib.SMTPRecipientsRefused:
        return False, "El servidor rechazó la dirección de destino. Verifica que esté bien escrita."
    except (smtplib.SMTPException, OSError) as error:
        # Mostramos el error real para poder diagnosticarlo
        print("Error técnico:", repr(error))
        return False, f"No se pudo conectar o enviar. Detalle: {error}"