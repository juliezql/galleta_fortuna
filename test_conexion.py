# test_conexion.py
# Script de diagnóstico: prueba cada forma de conectarse a Gmail.

import os
import smtplib
import socket
from dotenv import load_dotenv

load_dotenv()

remitente = os.getenv("EMAIL_REMITENTE")
password = (os.getenv("EMAIL_PASSWORD") or "").replace(" ", "")

print("Remitente:", remitente)
print("Largo de la clave:", len(password), "(una clave de aplicación de Gmail tiene 16)")
print()

# Prueba 1: ¿se puede abrir la conexión a cada puerto?
for puerto in (465, 587):
    try:
        socket.create_connection(("smtp.gmail.com", puerto), timeout=10).close()
        print(f"Puerto {puerto}: ABIERTO")
    except OSError as error:
        print(f"Puerto {puerto}: BLOQUEADO ->", error)
print()

# Prueba 2: login por 465 (SSL)
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as conexion:
        conexion.login(remitente, password)
    print("Login por 465 (SSL): OK")
except Exception as error:
    print("Login por 465 (SSL): FALLÓ ->", repr(error))

# Prueba 3: login por 587 (STARTTLS)
try:
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as conexion:
        conexion.starttls()
        conexion.login(remitente, password)
    print("Login por 587 (STARTTLS): OK")
except Exception as error:
    print("Login por 587 (STARTTLS): FALLÓ ->", repr(error))