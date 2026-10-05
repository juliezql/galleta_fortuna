# main.py
# Archivo principal: crea la ventana y conecta los botones con las funciones.

import re
import tkinter as tk

from frases import frase_al_azar, frase_con_ia
from email_sender import enviar_frase

# Aquí se guarda la frase que salió en la galleta (vacía = aún no se abrió)
frase_actual = ""


def mostrar_mensaje(texto, color):
    """Muestra un mensaje de estado debajo de los botones."""
    etiqueta_mensaje.config(text=texto, fg=color)


def email_valido(email):
    """Comprobación básica: algo@dominio.ext"""
    patron = r"^[\w\.\-\+]+@[\w\-]+(\.[\w\-]+)+$"
    return re.match(patron, email) is not None


def abrir_galleta():
    """Elige una frase de la lista y la muestra."""
    global frase_actual
    frase_actual = frase_al_azar()
    etiqueta_frase.config(text=frase_actual)
    mostrar_mensaje("¡Galleta abierta!", "green")


def generar_con_ia():
    """Intenta generar una frase nueva con IA; si falla, usa la lista."""
    global frase_actual
    mostrar_mensaje("Generando frase con IA...", "gray")
    ventana.update()  # refresca la ventana para que se vea el mensaje

    nueva = frase_con_ia()
    if nueva:
        frase_actual = nueva
        mostrar_mensaje("¡Frase nueva generada con IA!", "green")
    else:
        frase_actual = frase_al_azar()
        mostrar_mensaje("IA no disponible (¿falta la API Key?). Se usó una frase de la lista.", "orange")

    etiqueta_frase.config(text=frase_actual)


def enviar_por_email():
    """Valida los datos y envía la frase por correo."""
    email = campo_email.get().strip()

    # Validaciones
    if frase_actual == "":
        mostrar_mensaje("Primero abre una galleta.", "red")
        return
    if email == "":
        mostrar_mensaje("Escribe tu correo electrónico.", "red")
        return
    if not email_valido(email):
        mostrar_mensaje("El correo no tiene un formato válido (ej: nombre@gmail.com).", "red")
        return

    # Envío
    mostrar_mensaje("Enviando correo...", "gray")
    ventana.update()

    exito, texto = enviar_frase(email, frase_actual)
    mostrar_mensaje(texto, "green" if exito else "red")


# ---------------- INTERFAZ ----------------
COLOR_FONDO = "#FFF4E0"

ventana = tk.Tk()
ventana.title("Galleta de la Fortuna")
ventana.geometry("520x520")
ventana.config(bg=COLOR_FONDO)

tk.Label(ventana, text="🍪 Galleta de la Fortuna",
         font=("Arial", 22, "bold"), bg=COLOR_FONDO, fg="#8B4513").pack(pady=15)

tk.Button(ventana, text="Abrir galleta", font=("Arial", 13),
          bg="#F4A460", command=abrir_galleta).pack(pady=5)

tk.Button(ventana, text="✨ Generar frase nueva con IA", font=("Arial", 11),
          command=generar_con_ia).pack(pady=5)

etiqueta_frase = tk.Label(ventana, text="Aquí aparecerá tu frase...",
                          font=("Georgia", 14, "italic"), bg="white",
                          wraplength=440, height=5, relief="groove")
etiqueta_frase.pack(pady=15, padx=20, fill="x")

tk.Label(ventana, text="Tu correo electrónico:",
         font=("Arial", 11), bg=COLOR_FONDO).pack()

campo_email = tk.Entry(ventana, font=("Arial", 12), width=35)
campo_email.pack(pady=5)

tk.Button(ventana, text="Enviar frase por email", font=("Arial", 13),
          bg="#90EE90", command=enviar_por_email).pack(pady=10)

etiqueta_mensaje = tk.Label(ventana, text="", font=("Arial", 11),
                            bg=COLOR_FONDO, wraplength=460)
etiqueta_mensaje.pack(pady=5)

ventana.mainloop()