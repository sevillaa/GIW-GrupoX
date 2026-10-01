"""
TODO: rellenar

Asignatura: GIW
Práctica 3
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

import html
import xml.sax
from xml.etree import ElementTree


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

    
#Ejercicio 2
class _HandlerCategorias(xml.sax.ContentHandler):

    def __init__(self):
        super().__init__()
        self.in_Categoria = False
        self.in_SubCategoria = False
        self.categoria_nombre = []
        self.subcategoria_nombre = []
        self.categoria_actual = ""#Guarda el nombre de la categoria para recordarla entre subcategorias
        self.in_item = False

    def startElement(self, name, attrs):

        if name.lower() == "categoria":
            self.in_Categoria = True
        elif name.lower() == "subcategoria":
            self.in_SubCategoria = True
        elif name.lower() == "item":
            label = attrs.get("name")
            if label.lower() == "categoria":
                self.in_item = True
                self.categoria_nombre = []
            elif label.lower() == "subcategoria":
                self.in_item = True
                self.subcategoria_nombre = []


    def characters(self, content):
        if self.in_Categoria and not self.in_SubCategoria and self.in_item:
            self.categoria_nombre.append(content) 
        elif self.in_SubCategoria and self.in_Categoria and self.in_item:
            self.subcategoria_nombre.append(content)

    def endElement(self, name):

        if name.lower() == "item":
            if self.in_Categoria and not self.in_SubCategoria:
                self.categoria_actual = "".join(self.categoria_nombre)
            self.in_item = False
        elif name.lower() == "categoria":
            self.in_Categoria = False
        elif name.lower() == "subcategoria":
            print(f" '{self.categoria_actual} > {"".join(self.subcategoria_nombre)}' ")
            #Al encontrar que termina la subcategoria muestra todo por pantalla directamente para que sea mas simple
            self.in_SubCategoria = False
        



def subcategorias(filename):
    """Muestra todas todas las subcategorias de todos los restaurantes"""

    handler = _HandlerCategorias()
    xml.sax.parse(filename, handler)

subcategorias("./restaurantes_v1_es_pretty.xml")


def info_restaurante(filename, name):
    """Devuelve un diccionario con la información del restaurante si existe,
    o None si no existe en el fichero"""
    arbol = ElementTree.parse(filename)

    nombre = html.unescape(name).strip()

    for service in arbol.iter("service"): #Recorre todos los restaurantes
        nodo_nombre = service.find(".//name") #Busca <name> dentro de ese restaurante,
        if nodo_nombre is None or not nodo_nombre.text: #y si no tiene nombre o está vacío se salta
            continue

        nombre_actual = html.unescape(nodo_nombre.text).strip()

        # Si es el restaurante buscado, se actualizan el resto de etiquetas
        if nombre_actual == nombre:
            resultado = {"nombre": nombre_actual}
            datos = {
                "descripcion": ".//body",
                "email": ".//email",
                "web": ".//web",
                "phone": ".//phone",
                "horario": ".//Horario",
            }

            for clave, ruta in datos.items():
                nodo = service.find(ruta)
                if clave == "horario" and nodo is None:
                    nodo = service.find('.//item[@name="Horario"]')
                if nodo is not None and nodo.text:
                    texto = html.unescape(nodo.text).strip()
                    resultado[clave] = texto if texto else None
                else:
                    resultado[clave] = None

            return resultado

    return None


def busqueda_cercania(filename, lugar, n):
    ...

if __name__ == "__main__":
    infoRestaurante = info_restaurante(
        "restaurantes_v1_es_pretty.xml", "La Charca Restaurante"
    )
    print(infoRestaurante)
