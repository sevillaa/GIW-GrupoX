"""
TODO: rellenar

Asignatura: GIW
Práctica 3
Grupo: 10
Autores: Adrián Muñoz Rodríguez 

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""

import html
import xml.sax

class _HandlerRestaurante(xml.sax.ContentHandler):

    def __init__(self): #Inicializador de la clase
        super().__init__()
        self.in_name = False #bandera para saber si estamos dentro de <name>
        self.current_text  = [] #acumulador nom
        self.names = [] #lista final

    def startElement(self, name, attrs):

        #el dataset usa <name> para cada nombre en <basicData>
        if name.lower() == "name":
            self.in_name = True
            self.current_text = []

    def characters(self, content):
        if self.in_name:
            self.current_text.append(content)

    


def subcategorias(filename):
    ...


def info_restaurante(filename, name):
    ...


def busqueda_cercania(filename, lugar, n):
    ...
