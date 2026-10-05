# Galleta de la Fortuna

Aplicación de escritorio desarrollada en Python con Tkinter. Permite abrir una galleta de la fortuna virtual, obtener una frase motivacional (de una lista propia o generada con IA) y enviarla por correo electrónico.

Proyecto realizado con fines educativos para la Expo Técnica en la Institución Técnica 2 Rodolfo Walsh, con código simple y comentado: funciones, listas, condicionales, `try/except` y módulos separados.

## Características

- Más de 30 frases motivacionales en español, almacenadas en una lista.
- Generación opcional de frases nuevas con la API de Google Gemini (plan gratuito).
- Funcionamiento completo sin API Key: si la IA no está configurada o falla, se usa la lista de frases.
- Envío de la frase por correo mediante SMTP, con reintento automático por un segundo puerto.
- Validaciones: galleta abierta, correo no vacío y formato de correo válido.
- Manejo de errores de red y de autenticación sin cerrar el programa.
- Credenciales fuera del código, mediante un archivo `.env`.
- Script de diagnóstico para verificar la conexión con Gmail.

## Requisitos

- Python 3.9 o superior (Tkinter viene incluido en la instalación oficial para Windows).
- Una cuenta de Gmail con verificación en dos pasos activada.
- Conexión a internet.
- Opcional: una API Key de Google AI Studio para la generación de frases con IA.

## Instalación

1. Clonar o descargar el repositorio y ubicarse en la carpeta del proyecto:

   ```
   git clone https://github.com/TU_USUARIO/galleta_fortuna.git
   cd galleta_fortuna
   ```

2. Crear el entorno virtual:

   ```
   python -m venv venv
   ```

3. Activar el entorno virtual en Windows:

   ```
   venv\Scripts\activate
   ```

   En PowerShell:

   ```
   venv\Scripts\Activate.ps1
   ```

   Si PowerShell bloquea la ejecución de scripts, ejecutar una vez `Set-ExecutionPolicy -Scope Process RemoteSigned` y activar nuevamente. El entorno está activo cuando el prompt muestra `(venv)`.

4. Instalar las dependencias:

   ```
   pip install -r requirements.txt
   ```

## Configuración

### 1. Crear el archivo `.env`

Copiar el archivo de ejemplo y completar los datos:

```
copy .env.example .env
```

Contenido del archivo:

```
EMAIL_REMITENTE=tu_correo@gmail.com
EMAIL_PASSWORD=contrasena_de_aplicacion_sin_espacios
SMTP_SERVER=smtp.gmail.com
GEMINI_API_KEY=
```

Reglas de formato: sin comillas, sin espacios alrededor del `=` y sin extensión adicional en el nombre del archivo (debe llamarse exactamente `.env`).

| Variable | Descripción | Obligatoria |
|---|---|---|
| `EMAIL_REMITENTE` | Dirección de Gmail desde la que se envían los correos | Sí |
| `EMAIL_PASSWORD` | Contraseña de aplicación de esa misma cuenta | Sí |
| `SMTP_SERVER` | Servidor SMTP (`smtp.gmail.com` para Gmail) | No (valor por defecto) |
| `GEMINI_API_KEY` | Clave de la API de Gemini | No |

### 2. Obtener la contraseña de aplicación de Gmail

Gmail no permite iniciar sesión desde programas con la contraseña normal de la cuenta. Se debe generar una contraseña de aplicación, de uso exclusivo para este proyecto.

1. Ingresar a https://myaccount.google.com con la cuenta que actuará como remitente.
2. Ir a **Seguridad** y activar la **Verificación en dos pasos**. Sin este paso, la opción de contraseñas de aplicación no está disponible.
3. Ingresar a https://myaccount.google.com/apppasswords. Si no se encuentra, buscar "Contraseñas de aplicaciones" en el buscador de la cuenta.
4. Escribir un nombre para identificarla (por ejemplo, `Galleta de la Fortuna`) y presionar **Crear**.
5. Google muestra una clave de 16 caracteres. Copiarla sin espacios en la variable `EMAIL_PASSWORD`.

La clave se muestra una sola vez. Si se pierde o se expone, se debe eliminar desde la misma página y generar una nueva.

Si la opción no aparece, las causas habituales son: verificación en dos pasos desactivada, cuenta de Google Workspace (institucional) con la función bloqueada por el administrador, o Protección Avanzada activada. En esos casos conviene usar una cuenta personal de Gmail.

La contraseña de aplicación debe pertenecer a la misma cuenta indicada en `EMAIL_REMITENTE`.

### 3. Obtener la API Key de Gemini (opcional)

Esta clave habilita el botón "Generar frase nueva con IA". Si no se configura, el programa sigue funcionando con la lista de frases.

1. Ingresar a https://aistudio.google.com/app/apikey con una cuenta de Google.
2. Presionar **Create API key** y elegir o crear un proyecto.
3. Copiar la clave y pegarla en `GEMINI_API_KEY` dentro del archivo `.env`.

El plan gratuito no requiere tarjeta, pero tiene límites de uso por minuto y por día que Google puede modificar. Los valores vigentes se consultan en el panel de AI Studio. Se recomienda aplicar las restricciones de clave que ofrece Google al crearla.

## Ejecución

Con el entorno virtual activado y desde la carpeta del proyecto:

```
python main.py
```

## Uso

1. Presionar **Abrir galleta** para obtener una frase de la lista, o **Generar frase nueva con IA** para pedir una a Gemini.
2. Escribir el correo electrónico de destino en el campo correspondiente.
3. Presionar **Enviar frase por email**.
4. Leer el mensaje de estado que aparece debajo de los botones.

Para una primera prueba, se puede usar la propia dirección de correo como destinatario. Si el mensaje no llega, revisar la carpeta de spam.

Mensajes de validación esperados:

- Sin galleta abierta: "Primero abre una galleta."
- Campo de correo vacío: "Escribe tu correo electrónico."
- Formato incorrecto (por ejemplo `hola@`): mensaje de formato inválido.

## Diagnóstico de conexión

El script `test_conexion.py` verifica por separado la apertura de los puertos 465 y 587 y el inicio de sesión en Gmail, mostrando el error técnico de cada intento:

```
python test_conexion.py
```

Interpretación de los resultados más comunes:

| Resultado | Causa probable | Solución |
|---|---|---|
| Puerto bloqueado o `timed out` | Firewall o restricciones de la red | Probar con otra red o con los datos del celular |
| `Connection unexpectedly closed` | Antivirus que analiza conexiones SSL, o filtro de red | Desactivar temporalmente el escudo de correo del antivirus y repetir la prueba |
| `SMTPAuthenticationError` o `535` | Contraseña incorrecta o de otra cuenta | Generar una nueva contraseña de aplicación |
| Largo de clave distinto de 16 | Clave mal copiada | Revisar el `.env` |
| `getaddrinfo failed` | Servidor SMTP mal escrito | Verificar `SMTP_SERVER` |

## Estructura del proyecto

```
galleta_fortuna/
├── venv/               Entorno virtual (no se sube al repositorio)
├── main.py             Interfaz gráfica y validaciones
├── email_sender.py     Envío del correo por SMTP
├── frases.py           Lista de frases y generación con IA
├── test_conexion.py    Script de diagnóstico de conexión
├── requirements.txt    Dependencias del proyecto
├── .env                Credenciales reales (no se sube al repositorio)
├── .env.example        Plantilla de configuración sin datos reales
├── .gitignore          Archivos excluidos del control de versiones
└── README.md           Documentación
```

## Seguridad

- Las credenciales se leen desde variables de entorno y nunca se escriben en el código.
- El archivo `.env` está incluido en `.gitignore` y no debe subirse a GitHub bajo ninguna circunstancia. Antes del primer `git add .`, comprobar que `.gitignore` existe, y revisar con `git status` que `.env` no figure en la lista.
- Se utiliza una contraseña de aplicación y no la contraseña real de la cuenta. Se recomienda una cuenta de Gmail dedicada al proyecto.
- Si una clave se expone por error, eliminarla desde el panel correspondiente (Google Account o AI Studio) y generar una nueva. Borrar el archivo del repositorio no es suficiente, porque el historial de Git conserva su contenido.

## Dependencias

- `python-dotenv`: lectura del archivo `.env`.
- `google-genai`: cliente oficial de la API de Gemini.
