"""
Asignatura: GIW
Práctica 2
Grupo: 10
Autores: Izan de Vega, Miguel

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""

# https://docs.python.org/3/library/csv.html
import csv
import json
from pprint import pprint

from geopy.geocoders import Photon
from geopy import distance


### Formato CSV
def lee_fichero_accidentes(ruta):
    '''Lee un fichero csv con delimitador ';' y en el que la cabecera marca las claves de un 
    diccionario y los valores vienen dados por los valores en la misma posición de las 
    siguientes filas. 
    De forma que devuelve un array de diccionarios a partir del fichero en 'ruta' 
    '''
    with open(ruta, "r", newline='', encoding='utf8') as fich:
        # DictReader reads the csv as a dictionary.
        # Keys are first row, values of each key are in the rest of rows in the same idx as the key
        lector = csv.DictReader(fich, delimiter=';')
        whole_list = list(lector)
        return whole_list

def accidentes_por_distrito_tipo(datos):
    '''given a list of dictionary returns the number of accidents of each type on each district
    This uses keys: "distrito" and "tipo_accidente" and returns a dictionary whose keys are
    ("distrito","tipo_accidente") and value is the number of "tipo_accidente" 
    in "distrito" in "datos"
    '''
    ret_val = {}
    for val in datos:
        if (val["distrito"],val["tipo_accidente"]) not in ret_val:
            ret_val[(val["distrito"],val["tipo_accidente"])] = 1
        else:
            ret_val[(val["distrito"], val["tipo_accidente"])] += 1
    return ret_val


def dias_mas_accidentes(datos):
    '''Returns a dictionary with pair of key values in which 
    the keys are a date and 
    the values are the number of accidents in the given date
    This dictionary has the day of days with the highest ammount of accidents'''
    ret_val = {}
    greatest_value = 0
    for val in datos:
        if not val["fecha"] in ret_val:
            ret_val[val["fecha"]] = 1
            greatest_value = max(greatest_value, 1)
        else:
            ret_val[val["fecha"]] += 1
            greatest_value = max(ret_val[val["fecha"]], greatest_value)

    return [(key,value) for key,value in ret_val.items() if value == greatest_value]

def puntos_negros_distrito(datos, distrito, k):
    '''returns a list of pairs. The first element of the pair contains the concrete point 
    of the accident. The second contains the number of incidents in that concrete point. 
    Returns the top k pairs.
    Ordering in descending order by number of accidents, and alphabetically in case of draw'''
    ret_val={}
    for val in datos:
        if val["distrito"] == distrito:
            if val["localizacion"] not in ret_val:
                ret_val[val["localizacion"]] = 1
            else:
                ret_val[val["localizacion"]] += 1
    # items() returns a pair(key,value) dictionary view
    # its connected (shares elements) to the dictionary, that's why we gotta use 'list()'
    array_ret_val = list(ret_val.items())
    # orders by descendant value and alphabetically in case of draw
    def ordering_func(word):
        return (word[1],word[0])
    array_ret_val.sort(key=ordering_func, reverse=True)
    return [array_ret_val[i] for i in range(0,k)]

#### Formato JSON
def leer_monumentos(ruta):
    """Lee el fichero JSON y devuelve su lista de monumentos."""
    with open(ruta, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)
    return datos["@graph"]


def obtener_cantidad(pareja):
    """Devuelve la cantidad, situada en la segunda posición de la pareja."""
    return pareja[1]


def codigos_postales(monumentos):
    """
    Devuelve una lista de parejas (código postal, número de monumentos),
    ordenada de mayor a menor por número de monumentos.
    En caso de empate, conserva el orden de primera aparición.
    """
    conteo = {}

    for monumento in monumentos:
        codigo = monumento["address"]["postal-code"]

        if codigo not in conteo:
            conteo[codigo] = 1
        else:
            conteo[codigo] += 1

    resultado = list(conteo.items())
    resultado.sort(key=obtener_cantidad, reverse=True)

    return resultado


def busqueda_palabras_clave(monumentos, palabras):
    """
    Devuelve un conjunto de parejas (título, distrito) de los monumentos
    que contienen todas las palabras clave entre su título y descripción,
    sin distinguir mayúsculas y minúsculas.
    Si no existe el distrito, utiliza una cadena vacía.
    """
    resultado = set()

    for monumento in monumentos:
        titulo = monumento["title"]
        descripcion = monumento["organization"]["organization-desc"]

        titulo_minusculas = titulo.lower()
        descripcion_minusculas = descripcion.lower()
        cumple = True

        for palabra in palabras:
            palabra = palabra.lower()

            if palabra not in titulo_minusculas and palabra not in descripcion_minusculas:
                cumple = False
                break

        if cumple:
            distrito = monumento.get("address", {}).get("district", {}).get("@id", "")
            resultado.add((titulo, distrito))

    return resultado


def obtener_distancia(terna):
    """Devuelve la distancia, situada en la tercera posición."""
    return terna[2]


def busqueda_distancia(monumentos, direccion, distancia):
    """
    Devuelve una lista de ternas (título, id, distancia en kilómetros)
    de los monumentos a menos de la distancia indicada desde la dirección.
    Ordena de más cercano a más lejano, conservando el orden original
    en caso de empate. Ignora los monumentos sin coordenadas.
    """
    resultado = []

    geolocalizador = Photon(user_agent="giw_practica2", timeout=10)
    ubicacion = geolocalizador.geocode(direccion)

    if ubicacion is None:
        return resultado

    origen = (ubicacion.latitude, ubicacion.longitude)

    for monumento in monumentos:
        localizacion = monumento.get("location", {})
        latitud = localizacion.get("latitude")
        longitud = localizacion.get("longitude")

        if latitud is None or longitud is None:
            continue

        destino = (latitud, longitud)
        kilometros = distance.distance(origen, destino).km

        if kilometros < distancia:
            resultado.append(
                (monumento["title"], monumento["id"], kilometros)
            )

    resultado.sort(key=obtener_distancia)

    return resultado


if __name__ == "__main__":
    pprint("Ejercicio 1:")

    data = lee_fichero_accidentes("AccidentesBicicletas_2025.csv")
    pprint("Accidentes por distrito: ")
    pprint(accidentes_por_distrito_tipo(data))
    pprint("Dias con más accidentes: ")
    pprint(dias_mas_accidentes(data))
    pprint("Top 16 puntos negros Moncloa-Aravaca")
    pprint(puntos_negros_distrito(data, "MONCLOA-ARAVACA", 16))

    print("\nEjercicio 2:")
    monumentos = leer_monumentos("300356-2-monumentos-ciudad-madrid-json.json")
    print("Monumentos leídos:", len(monumentos))

    print("Primeros cinco códigos postales:")
    pprint(codigos_postales(monumentos)[:5])

    print("Búsqueda de palabras clave:")
    pprint(busqueda_palabras_clave(monumentos, ["Alfonso", "XII"]))

    print("Monumentos a menos de 1 km de la facultad:")
    pprint(busqueda_distancia(
        monumentos, "Profesor José García Santesmases 9, Madrid, España", 1
    ))
