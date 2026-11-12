"""
Asignatura: GIW
Práctica 10
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

from flask import Flask, request, session
# Resto de importaciones


app = Flask(__name__,
            static_folder='static',      # Ficheros estáticos
            template_folder='templates') # Plantillas


# Credenciales
CLIENT_ID = 'XXXXXX'
CLIENT_SECRET = 'YYYYYY'

REDIRECT_URI = 'http://localhost:5000/token'

# Fichero de descubrimiento para obtener el 'authorization endpoint' y el 
# 'token endpoint'
DISCOVERY_DOC = 'https://accounts.google.com/.well-known/openid-configuration'


@app.route('/login_google', methods=['GET'])
def login_google():
    ...


@app.route('/token', methods=['GET'])
def token():
    ...

        
if __name__ == '__main__':
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'giw_clave_secreta'
    app.run(debug=True)

