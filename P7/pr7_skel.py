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

from itertools import count

from flask import Flask, request, jsonify

app = Flask(__name__)

# Diccionario de asignaturas: id -> {nombre, numero_alumnos, horario}
asignaturas = {}
# Generador de IDs únicos e incrementales desde 0 (nunca decrece)
ID_GEN = count()

# --- Funciones de validación ---

def es_int(valor):
    """Comprueba que es int pero no bool"""
    return isinstance(valor, int) and not isinstance(valor, bool)

def es_horario_valido(horario):
    """Valida un bloque {dia, hora_inicio, hora_final}"""
    if not isinstance(horario, dict) or len(horario) != 3:
        return False

    for campo in ("dia", "hora_inicio", "hora_final"):
        if campo not in horario:
            return False

    if not isinstance(horario["dia"], str):
        return False
    if not es_int(horario["hora_inicio"]) or not es_int(horario["hora_final"]):
        return False
    return True

def es_lista_horarios_valida(horarios):
    """Comprueba que todos los bloques de la lista tienen el formato correcto"""
    if not isinstance(horarios, list):
        return False
    for horario in horarios:
        if not es_horario_valido(horario):
            return False
    return True

def es_asig_valida(datos):
    """Exactamente nombre(str), numero_alumnos(int) y horario(lista de bloques válidos)"""
    if not isinstance(datos, dict) or len(datos) != 3:
        return False

    for campo in ("nombre", "numero_alumnos", "horario"):
        if campo not in datos:
            return False

    if not isinstance(datos["nombre"], str) or not es_int(datos["numero_alumnos"]):
        return False
    return es_lista_horarios_valida(datos["horario"])

def es_patch_valido(datos):
    """Comprueba que se modifica un único campo y que su valor es válido"""
    if not isinstance(datos, dict) or len(datos) != 1:
        return False

    if "nombre" in datos:
        return isinstance(datos["nombre"], str)
    if "numero_alumnos" in datos:
        return es_int(datos["numero_alumnos"])
    if "horario" in datos:
        return es_lista_horarios_valida(datos["horario"])
    return False

def parsear_parametros(args):
    """Devuelve (alumnos_gte, page, per_page) o None si son incorrectos"""
    for clave in args:
        if clave not in ("alumnos_gte", "page", "per_page"):
            return None
    # page y per_page deben aparecer siempre juntos
    if ("page" in args) != ("per_page" in args):
        return None
    try:
        valores = {}
        for clave, valor in args.items():
            valores[clave] = int(valor)
    except ValueError:
        return None
    if valores.get("page", 1) < 1 or valores.get("per_page", 1) < 1:
        return None
    return valores.get("alumnos_gte"), valores.get("page"), valores.get("per_page")


# --- 2.1 /asignaturas ---

@app.route('/asignaturas', methods=['GET'])
def listar_asignaturas():
    """Lista las URL de las asignaturas, con filtro y paginado opcionales"""
    params = parsear_parametros(request.args)
    if params is None:
        return '', 400
    minimo, pagina, tam_pagina = params
    # Los dicts conservan el orden de inserción
    rutas = []
    for identificador, asignatura in asignaturas.items():
        if minimo is None or asignatura["numero_alumnos"] >= minimo:
            rutas.append(f"/asignaturas/{identificador}")
    # El paginado se aplica después del filtro
    if pagina is not None:
        inicio = (pagina - 1) * tam_pagina
        rutas = rutas[inicio:inicio + tam_pagina]
    return jsonify({"asignaturas": rutas})


@app.route('/asignaturas', methods=['POST'])
def crear_asignatura():
    """Crea una asignatura y devuelve su id"""
    datos = request.get_json(silent=True)
    #silent=True: devuelve None (en vez de lanzar error) si no hay JSON válido
    if not es_asig_valida(datos):
        return '', 400
    identificador = next(ID_GEN)
    asignaturas[identificador] = datos
    return jsonify({"id": identificador}), 201


@app.route('/asignaturas', methods=['DELETE'])
def borrar_asignaturas():
    """Borra todas las asignaturas"""
    asignaturas.clear()
    return '', 204


# --- 2.2 /asignaturas/X ---

@app.route('/asignaturas/<int:identificador>', methods=['GET'])
def obtener_asignatura(identificador):
    """Devuelve los datos de una asignatura"""
    if identificador not in asignaturas:
        return '', 404
    resultado = asignaturas[identificador].copy()
    resultado["id"] = identificador
    return jsonify(resultado)


@app.route('/asignaturas/<int:identificador>', methods=['DELETE'])
def borrar_asignatura(identificador):
    """Borra una asignatura"""
    if identificador not in asignaturas:
        return '', 404
    del asignaturas[identificador]
    return '', 204


@app.route('/asignaturas/<int:identificador>', methods=['PUT'])
def reemplazar_asignatura(identificador):
    """Reemplaza una asignatura entera conservando su id"""
    if identificador not in asignaturas:
        return '', 404
    datos = request.get_json(silent=True)
    if not es_asig_valida(datos):
        return '', 400
    asignaturas[identificador] = datos
    resultado = datos.copy()
    resultado["id"] = identificador
    return jsonify(resultado)


@app.route('/asignaturas/<int:identificador>', methods=['PATCH'])
def modificar_asignatura(identificador):
    """Modifica un único campo de una asignatura"""
    if identificador not in asignaturas:
        return '', 404
    datos = request.get_json(silent=True)
    if not es_patch_valido(datos):
        return '', 400
    asignaturas[identificador].update(datos)
    resultado = asignaturas[identificador].copy()
    resultado["id"] = identificador
    return jsonify(resultado)


# --- 2.3 /asignaturas/X/horario ---

@app.route('/asignaturas/<int:identificador>/horario', methods=['GET'])
def horario_asignatura(identificador):
    """Devuelve únicamente el horario de una asignatura concreta"""
    if identificador not in asignaturas:
        return '', 404
    return jsonify({"horario": asignaturas[identificador]["horario"]})


if __name__ == '__main__':
    app.run(debug=True)
