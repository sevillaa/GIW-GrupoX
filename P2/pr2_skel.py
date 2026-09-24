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

import csv;
import json;
from pprint import pprint

### Formato CSV
def lee_fichero_accidentes(ruta):
    '''Lee un fichero csv con delimitador ';' y en el que la cabecera marca las claves de un diccionario
    y los valores vienen dados por los valores en la misma posición de las siguientes filas.
    De forma que devuelve un array de diccionarios a partir del fichero en 'ruta' 
    '''
    with open(ruta, "r", newline='', encoding='utf8') as fich:
        lector = csv.DictReader(fich, delimiter=';')
        whole_list = list(lector)
        return whole_list

def accidentes_por_distrito_tipo(datos):
    ...

def dias_mas_accidentes(datos):
    ...

def puntos_negros_distrito(datos, distrito, k):
    ...


#### Formato JSON
def leer_monumentos(ruta):
    
    with open('300356-2-monumentos-ciudad-madrid-json.json', 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)
    print(datos)

    
    

def codigos_postales(monumentos):
    ...

def busqueda_palabras_clave(monumentos, palabras):
    ...

def busqueda_distancia(monumentos, direccion, distancia):
    ...

if __name__ == "__main__":
    pprint(lee_fichero_accidentes("AccidentesBicicletas_2025.csv"))
