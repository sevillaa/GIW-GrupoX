"""
TODO: rellenar

Asignatura: GIW
Práctica 2
Grupo: 10
Autores: Izan de Vega

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""

# https://docs.python.org/3/library/csv.html
import csv

from pprint import pprint

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
                ret_val[val["localizacion"]] = 0
            else:
                ret_val[val["localizacion"]] += 1
    # items() returns a pair(key,value) dictionary view
    # its connected (shares elements) to the dictionary, that's why we gotta use 'list()'
    array_ret_val = list(ret_val.items())
    # orders by descendant value and alphabetically in case of draw
    array_ret_val.sort(key=lambda x: (-x[1], x[0]))
    return [array_ret_val[i] for i in range(0,k)]

#### Formato JSON
def leer_monumentos(ruta):
    with open(ruta, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)
    print(datos)


def codigos_postales(monumentos):
    ...

def busqueda_palabras_clave(monumentos, palabras):
    ...

def busqueda_distancia(monumentos, direccion, distancia):
    ...

if __name__ == "__main__":
    pprint("Ejercicio 1:")

    data = lee_fichero_accidentes("AccidentesBicicletas_2025.csv")
    pprint("Accidentes por distrito: ")
    pprint(accidentes_por_distrito_tipo(data))
    pprint("Dias con más accidentes: ")
    pprint(dias_mas_accidentes(data))
    pprint("Top 5 puntos negros Centro")
    pprint(puntos_negros_distrito(data, "CENTRO", 5))

    pprint("Ejercicio 2:")
    # leer_monumentos("300356-2-monumentos-ciudad-madrid-json.json")
