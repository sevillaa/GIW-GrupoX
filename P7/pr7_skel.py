"""
TODO: rellenar

Asignatura: GIW
Práctica X
Grupo: XXXXXXX
Autores: XXXXXX 

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""

from flask import Flask, request, session, render_template, jsonify
import requests
from pprint import pp 
app = Flask(__name__)

url = 'http://localhost:5000'

def muestra(r):
    print(r.status_code, r.reason)
    if r.content:
        pp(r.json())


###
asignaturas = {
    'GIW': {
        'id': '1',
        'nombre': 'Gestión de la Información en la Web',
        'numero_alumnos':100,
        'horario':{
            'dia':'Lunes',
            'hora_inicio':'10:00',
            'hora_fin':'12:00'
        }
    },
}

@app.route('/asignaturas', methods=['GET'])
def get():
    """Devuelve la lista de asignaturas"""  
    return {'asignaturas': asignaturas}

###


if __name__ == '__main__':
    # Activa depurador y recarga automáticamente
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TEST'] = True

    # Imprescindible para usar sesiones
    app.config['SECRET_KEY'] = 'giw_clave_secreta'

    app.config['STATIC_FOLDER'] = 'static'
    app.config['TEMPLATES_FOLDER'] = 'templates'

    app.run()

