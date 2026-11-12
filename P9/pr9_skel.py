"""
TODO: rellenar

Asignatura: GIW
Práctica 9
Grupo: 10
Autores:  Miguel Sevilla Benito, Izan de Vega López,
            Adrián Muñoz Rodríguez, Israel Suárez Fraile, Oier Osorio Illarramendi 

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""


from flask import Flask, request, session, render_template
from mongoengine import connect, Document, StringField, EmailField
# Resto de importaciones
from mongoengine.errors import ValidationError
from argon2 import PasswordHasher
#Argon2 example
# >>> from argon2 import PasswordHasher
# >>> ph = PasswordHasher()
# >>> hash = ph.hash("correct horse battery staple")
# >>> hash  # doctest: +SKIP
# '$argon2id$v=19$m=65536,t=3,p=4$MIIRqgvgQbgj220jfp0MPA$YfwJSVjtjSU0zzV/P3S9nnQ/USre2wvJMjfCIjrTQbg'
# >>> ph.verify(hash, "correct horse battery staple")
# True
# >>> ph.check_needs_rehash(hash)
# False
# >>> ph.verify(hash, "Tr0ub4dor&3")
# Traceback (most recent call last):
#   ...
# argon2.exceptions.VerifyMismatchError: The password does not match the supplied hash


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

# 
# Todo: Ampliar explicación de pq usamos Argon2
# Usaremos Argon2 un método que usa hashing y sal
#

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

    if nickname and User.objects(user_id=nickname).first() is not None:
        return render_message("El usuario ya existe")

    if not nickname or not password:
        return render_message("Datos de usuario no válidos")

    try:
        hashed_password = PH.hash(password)
        new_user = User(
            user_id=nickname,
            full_name=full_name,
            country=country,email=email,
            passwd=hashed_password
        )
        new_user.save(force_insert=True)
    except ValidationError:
        return render_message("Datos de usuario no válidos")

    return render_message(f"Bienvenido usuario {full_name}")


@app.route('/change_password', methods=['POST'])
def change_password():
    ...
 
           
@app.route('/login', methods=['POST'])
def login():
    ...
    

##############
# APARTADO 2 #
##############

# 
# Explicación detallada de cómo se genera la semilla aleatoria, cómo se construye
# la URL de registro en Google Authenticator y cómo se genera el código QR
#


@app.route('/signup_totp', methods=['POST'])
def signup_totp():
    ...
        

@app.route('/login_totp', methods=['POST'])
def login_totp():
    ...
  

if __name__ == '__main__':
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'giw_clave_secreta'
    app.run(debug=True)

