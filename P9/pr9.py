"""
Asignatura: GIW
Práctica 9
Grupo: 10
Autores: Miguel Sevilla Benito, Izan de Vega López,
         Adrián Muñoz Rodríguez, Israel Suárez Fraile, Oier Osorio Illarramendi

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""

import base64
import html
import io

import pyotp
import qrcode
from flask import Flask, request
from mongoengine import connect, Document, StringField, EmailField
from mongoengine.errors import ValidationError
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError


app = Flask(__name__,
            static_folder='static',      # Ficheros estáticos
            template_folder='templates') # Plantillas
connect('giw_auth')

# Instancia global del hasher Argon2id con parámetros seguros por defecto
PH = PasswordHasher()


# Clase para almacenar usuarios usando mongoengine
# ** No es necesario modificarla **
class User(Document):
    """Esquema de usuario en MongoDB."""
    user_id = StringField(primary_key=True)
    full_name = StringField(min_length=2, max_length=50, required=True)
    country = StringField(min_length=2, max_length=50, required=True)
    email = EmailField(required=True)
    passwd = StringField(required=True)
    totp_secret = StringField(required=False)


def render_message(message: str) -> str:
    """Devuelve una página HTML mínima con el mensaje indicado."""
    return f"<!DOCTYPE html><html><body><p>{message}</p></body></html>"


def get_user(nickname: str):
    """Devuelve el usuario con ese nickname o None si no existe."""
    # mongoengine añade 'objects' a la clase en tiempo de ejecución mediante una
    # metaclase, por eso pylint no lo detecta (falso positivo de no-member)
    return User.objects(user_id=nickname).first()  # pylint: disable=no-member


##############
# APARTADO 1 #
##############

# Mecanismo de almacenamiento de contraseñas y justificación de seguridad:
#
# 1. Elección de la biblioteca (argon2-cffi):
#    Esta biblioteca envuelve la implementación oficial de referencia en
#    C de Argon2 (ganador de la Password Hashing Competition), cuenta con
#    mantenimiento activo, una API muy sencilla y gestiona automaticamente
#    la sal para cada contraseña almacenada.
#
# 2. Por qué es seguro (Argon2):
#    - Función hash unidireccional: las contraseñas nunca se guardan en texto claro
#      ni cifradas de forma reversible; ante una fuga de la base de datos no es
#      posible recuperar la clave original.
#    - Sal criptográfica única por usuario: argon2-cffi genera automáticamente una
#      sal aleatoria de 128 bits para cada contraseña. Esto
#      inutiliza ataques mediante tablas arcoíris y garantiza que dos usuarios con
#      la misma contraseña produzcan hashes completamente distintos.
#    - Exige un alto coste de memoria, iteraciones y paralelismo, haciendo
#      inviable el descifrado masivo por fuerza bruta.


@app.route('/signup', methods=['POST'])
def signup():
    """Da de alta a un nuevo usuario tras validar sus datos y hashear su clave."""
    nickname = request.form.get('nickname', '').strip()
    full_name = request.form.get('full_name', '').strip()
    country = request.form.get('country', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    password2 = request.form.get('password2', '')

    if password != password2:
        return render_message("Las contraseñas no coinciden")

    if nickname and get_user(nickname) is not None:
        return render_message("El usuario ya existe")

    if not nickname or not password:
        return render_message("Datos de usuario no válidos")

    try:
        hashed_password = PH.hash(password)
        new_user = User(
            user_id=nickname,
            full_name=full_name,
            country=country,
            email=email,
            passwd=hashed_password
        )
        new_user.save(force_insert=True)
    except ValidationError:
        return render_message("Datos de usuario no válidos")

    return render_message(f"Bienvenido usuario {full_name}")


@app.route('/change_password', methods=['POST'])
def change_password():
    """Actualiza la contraseña de un usuario tras verificar su clave actual."""
    nickname = request.form.get('nickname', '').strip()
    old_password = request.form.get('old_password', '')
    new_password = request.form.get('new_password', '')

    user = get_user(nickname)
    if user is None:
        return render_message("Usuario o contraseña incorrectos")

    try:
        PH.verify(user.passwd, old_password)
    except VerificationError:
        return render_message("Usuario o contraseña incorrectos")

    user.passwd = PH.hash(new_password)
    user.save()

    return render_message(f"La contraseña del usuario {nickname} ha sido modificada")


@app.route('/login', methods=['POST'])
def login():
    """Autentica a un usuario comprobando su identificador y contraseña."""
    nickname = request.form.get('nickname', '').strip()
    password = request.form.get('password', '')

    user = get_user(nickname)
    if user is None:
        return render_message("Usuario o contraseña incorrectos")

    try:
        PH.verify(user.passwd, password)
    except VerificationError:
        return render_message("Usuario o contraseña incorrectos")

    return render_message(f"Bienvenido {user.full_name}")


##############
# APARTADO 2 #
##############

# Generación de la semilla, de la URL de registro y del código QR:
#
# 1. Semilla aleatoria (secreto TOTP):
#    Se genera con pyotp.random_base32(), que internamente usa el módulo 'secrets'
#    de Python (un generador de números aleatorios criptográficamente seguro, CSPRNG)
#    para elegir 32 caracteres del alfabeto Base32 (A-Z y 2-7). Eso equivale a
#    160 bits de entropía, el tamaño recomendado por el RFC 4226 para HOTP/TOTP.
#    El secreto se guarda en el campo 'totp_secret' del usuario para que el
#    servidor pueda calcular después el código temporal y compararlo con el
#    que envía el usuario.
#
# 2. URL de registro en Google Authenticator:
#    Se construye con el método provisioning_uri() de pyotp.TOTP, que sigue el
#    formato "Key Uri Format" que entienden las apps de autenticación:
#        otpauth://totp/<emisor>:<usuario>?secret=<secreto>&issuer=<emisor>
#    El emisor (ISSUER) identifica nuestra aplicación y el usuario es su nickname,
#    de modo que la app muestre la cuenta como "GIW Grupo 10: nickname". Los
#    parámetros no indicados (algoritmo SHA1, 6 dígitos y periodo de 30 segundos)
#    toman los valores por defecto que usan todas las apps.
#
# 3. Código QR:
#    Se genera en el propio servidor con la biblioteca qrcode (qrcode.make),
#    que devuelve una imagen PIL que codifica la URL anterior. Así el secreto no
#    se envía nunca a un servicio externo. La imagen se guarda en formato PNG en
#    memoria (io.BytesIO, sin crear ficheros), se codifica en Base64 y se incrusta
#    directamente en la página HTML con una data URL:
#        <img src="data:image/png;base64,....">
#    Además, la página muestra el nickname y el secreto en texto plano por si el
#    usuario prefiere configurar la app a mano.

# Nombre de nuestra aplicación que verá el usuario en su app de autenticación
ISSUER = "GIW Grupo 10"


def generate_qr_base64(text: str) -> str:
    """Genera un código QR con el texto indicado y lo devuelve como PNG en Base64."""
    qr_image = qrcode.make(text)
    # Guardamos la imagen PNG en memoria en lugar de en un fichero
    buffer = io.BytesIO()
    qr_image.save(buffer, format="PNG")
    # b64encode devuelve bytes; decode() los convierte en str para meterlos en el HTML
    return base64.b64encode(buffer.getvalue()).decode("ascii")


@app.route('/signup_totp', methods=['POST'])
def signup_totp():
    """Da de alta a un usuario generando su secreto TOTP y código QR."""
    nickname = request.form.get('nickname', '').strip()
    full_name = request.form.get('full_name', '').strip()
    country = request.form.get('country', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    password2 = request.form.get('password2', '')

    # Mismas comprobaciones que en /signup
    if password != password2:
        return render_message("Las contraseñas no coinciden")

    if nickname and get_user(nickname) is not None:
        return render_message("El usuario ya existe")

    if not nickname or not password:
        return render_message("Datos de usuario no válidos")

    # Secreto aleatorio en Base32 que compartimos con la app del usuario
    secret = pyotp.random_base32()

    try:
        new_user = User(
            user_id=nickname,
            full_name=full_name,
            country=country,
            email=email,
            passwd=PH.hash(password),
            totp_secret=secret
        )
        new_user.save(force_insert=True)
    except ValidationError:
        return render_message("Datos de usuario no válidos")

    # URL otpauth:// que la app de autenticación sabe interpretar
    provisioning_url = pyotp.TOTP(secret).provisioning_uri(name=nickname, issuer_name=ISSUER)
    qr_base64 = generate_qr_base64(provisioning_url)

    # Escapamos los datos que escribe el usuario antes de meterlos en el HTML
    # para evitar que pueda inyectar código (XSS)
    return f"""<!DOCTYPE html>
    <html>
    <body>
    <p>Bienvenido usuario {html.escape(full_name)}</p>
    <p>Escanea este código QR con tu app de autenticación:</p>
    <img src="data:image/png;base64,{qr_base64}" alt="Código QR TOTP">
    <p>Si prefieres configurarla manualmente, usa estos datos:</p>
    <p>Usuario: {html.escape(nickname)}</p>
    <p>Secreto: {secret}</p>
    </body>
    </html>"""


@app.route('/login_totp', methods=['POST'])
def login_totp():
    """Autentica a un usuario mediante contraseña y código TOTP."""
    nickname = request.form.get('nickname', '').strip()
    password = request.form.get('password', '')
    totp_code = request.form.get('totp', '').strip()

    user = get_user(nickname)
    if user is None:
        return render_message("Usuario o contraseña incorrectos")

    try:
        PH.verify(user.passwd, password)
    except VerificationError:
        return render_message("Usuario o contraseña incorrectos")

    # Los usuarios dados de alta con /signup no tienen secreto TOTP
    if not user.totp_secret:
        return render_message("Usuario o contraseña incorrectos")

    # verify() calcula el código actual a partir del secreto y lo compara con el
    # recibido. valid_window=1 acepta también el código del intervalo de 30 s
    # anterior y posterior, para tolerar pequeños desfases de reloj con el móvil.
    if not pyotp.TOTP(user.totp_secret).verify(totp_code, valid_window=1):
        return render_message("Usuario o contraseña incorrectos")

    return render_message(f"Bienvenido {user.full_name}")


if __name__ == '__main__':
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'giw_clave_secreta'
    app.run(debug=True)
