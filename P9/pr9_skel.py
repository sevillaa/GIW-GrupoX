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


##############
# APARTADO 1 #
##############

# Mecanismo de almacenamiento de contraseñas y justificación de seguridad:
#
# 1. Elección de la biblioteca (argon2-cffi):
#    Frente a alternativas como hashlib (funciones hash generales demasiado rápidas
#    y sin gestión automática de sal), bcrypt (limitado a contraseñas de 72 bytes y
#    no resistente a ataques con hardware especializado con gran memoria) o passlib
#    (con menor actividad reciente), se ha elegido 'argon2-cffi'. Esta biblioteca
#    envuelve la implementación oficial de referencia en C de Argon2 (ganador de la
#    Password Hashing Competition), cuenta con mantenimiento activo, una API muy
#    sencilla y almacena en una única cadena autocontenida (formato PHC) el algoritmo,
#    versión, parámetros de coste, sal y resumen criptográfico.
#
# 2. Por qué es seguro (Argon2id):
#    - Función hash unidireccional: las contraseñas nunca se guardan en texto claro
#      ni cifradas de forma reversible; ante una fuga de la base de datos no es
#      posible recuperar la clave original.
#    - Sal criptográfica única por usuario: argon2-cffi genera automáticamente una
#      sal aleatoria de 128 bits (mediante un CSPRNG) para cada contraseña. Esto
#      inutiliza ataques mediante tablas arcoíris y garantiza que dos usuarios con
#      la misma contraseña produzcan hashes completamente distintos.
#    - Resistencia a fuerza bruta y hardware paralelo (memory-hard): Argon2id combina
#      Argon2i (acceso a memoria independiente de los datos, mitigando ataques de
#      canal lateral) y Argon2d (acceso dependiente de los datos, maximizando la
#      resistencia frente a GPUs y ASICs). Sus parámetros por defecto exigen un alto
#      coste de memoria (64 MiB), iteraciones (t=3) y paralelismo (p=4), haciendo
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

    if nickname and User.objects(user_id=nickname).first() is not None:  # pylint: disable=no-member
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

    user = User.objects(user_id=nickname).first()  # pylint: disable=no-member
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

    user = User.objects(user_id=nickname).first()  # pylint: disable=no-member
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

#
# Explicación detallada de cómo se genera la semilla aleatoria, cómo se construye
# la URL de registro en Google Authenticator y cómo se genera el código QR
#


@app.route('/signup_totp', methods=['POST'])
def signup_totp():
    """Da de alta a un usuario generando su secreto TOTP y código QR."""
    ...


@app.route('/login_totp', methods=['POST'])
def login_totp():
    """Autentica a un usuario mediante contraseña y código TOTP."""
    ...


if __name__ == '__main__':
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'giw_clave_secreta'
    app.run(debug=True)
