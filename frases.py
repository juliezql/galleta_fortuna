# frases.py
# Este módulo guarda las frases y sabe obtener una frase nueva con IA.

import os
import random
from dotenv import load_dotenv

# Lee el archivo .env y carga sus valores como variables de entorno
load_dotenv()

# Lista de frases predeterminadas (la app funciona siempre con estas)
FRASES = [
    "Cada pequeño esfuerzo de hoy es un paso hacia tu mejor versión de mañana.",
    "Estudiar hoy es sembrar las oportunidades que vas a cosechar mañana.",
    "No tienes que ser perfecto, solo tienes que ser constante.",
    "Los errores son la prueba de que estás intentando.",
    "Confía en tu proceso: aprender lleva tiempo y vale la pena.",
    "Lo difícil de hoy será tu fortaleza de mañana.",
    "El futuro pertenece a quienes se preparan para él desde hoy.",
    "Cada problema que resuelves te vuelve más capaz de resolver el siguiente.",
    "Si te caes siete veces, levántate ocho.",
    "Tu única competencia es la persona que fuiste ayer.",
    "Las grandes metas se logran con pequeños pasos diarios.",
    "Cree en ti: ya llegaste más lejos de lo que pensabas.",
    "Una oportunidad aparece cuando la preparación se encuentra con la acción.",
    "No te rindas: lo que hoy parece imposible mañana será tu logro.",
    "Aprender algo nuevo cada día te acerca a las puertas que quieres abrir.",
    "El éxito es la suma de pequeños esfuerzos repetidos día tras día.",
    "Tu actitud hoy define los resultados de mañana.",
    "Las dificultades no te detienen: te enseñan el camino.",
    "Empieza donde estás, con lo que tienes, y haz lo que puedas.",
    "La disciplina te lleva donde la motivación no alcanza.",
    "Un buen futuro se construye con las decisiones que tomas hoy.",
    "No midas tu progreso por la velocidad, sino por la dirección.",
    "Todo experto fue alguna vez un principiante que no se rindió.",
    "Cuando algo sale mal, respira, aprende y vuelve a intentarlo.",
    "Tu esfuerzo silencioso de hoy será tu aplauso de mañana.",
    "Las mejores oportunidades llegan a quienes están listos para aprovecharlas.",
    "Tener miedo es normal; avanzar a pesar de él es lo que te hace valiente.",
    "Estudiar no es una carga, es una inversión en tu libertad.",
    "Cada día es una nueva página para escribir tu historia.",
    "Lo que haces hoy puede cambiar todos tus mañanas.",
    "La paciencia y la perseverancia hacen desaparecer las dificultades.",
    "Eres capaz de más de lo que imaginas; solo necesitas empezar.",
]


def frase_al_azar():
    """Devuelve una frase cualquiera de la lista."""
    return random.choice(FRASES)


def frase_con_ia():
    """
    Pide una frase motivacional nueva a la IA (API de Google Gemini).
    Devuelve el texto de la frase, o None si no se pudo
    (sin API Key, sin internet, límite de uso, etc.).
    """
    api_key = os.getenv("GEMINI_API_KEY")

    # Si no hay clave configurada, no intentamos nada
    if not api_key:
        return None

    try:
        from google import genai

        cliente = genai.Client(api_key=api_key)
        respuesta = cliente.models.generate_content(
            model="gemini-3.8-flash",
            contents=(
                "Escribe UNA sola frase motivacional original en español, "
                "de máximo 25 palabras, pensada para un estudiante. "
                "Responde solo con la frase, sin comillas ni explicaciones."
            ),
        )
        texto = respuesta.text.strip().strip('"')
        return texto if texto else None

    except Exception as error:
        # Mostramos el error en la terminal para poder diagnosticarlo
        print("Error con la IA:", repr(error))
        return None