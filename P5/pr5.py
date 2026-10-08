"""
TODO: rellenar

Asignatura: GIW
Práctica 5
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


URL = 'https://books.toscrape.com/'

import requests


# APARTADO 1 #
def categorias():
    """ Devuelve un conjunto de parejas (nombre, número libros) de todas las categorías """
    res = requests.get(URL)
    try:
        res.raise_for_status()
        archivo = open("Archivo.txt","wb")
        for bloque in res.iter_content(10000):
        archivo.write(bloque)
        archivo.close()
    except:
        print ("Hubo un problema")


# APARTADO 2 #
def libros_categoria(nombre):
    """ Dado el nombre de una categoría, devuelve un conjunto de tuplas 
        (titulo, precio, valoracion), donde el precio será un número real y la 
        valoración un número natural """
    ...

