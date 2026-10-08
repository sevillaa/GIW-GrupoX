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
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
#Ejercicio 1
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

    def endElement(self, name):

        if name.lower() == "name" and self.in_name:

            raw = "".join(self.current_text)
            # Desescapar HTML + limpiar espacios
            cleaned = html.unescape(raw).strip()
            if cleaned:
                self.names.append(cleaned)

            # se resetea el estado
            self.in_name = False
            self.current_text = []

def nombres_restaurantes(filename):

    """devuelve la lista alfabetica de restaurantes"""
    parser = xml.sax.make_parser()
    h = _HandlerRestaurante()
    parser.setContentHandler(h)

    with open(filename, "r", encoding="utf-8") as f:
        parser.parse(f)
    return sorted(h.names)

#Ejercicio 2
class _HandlerCategorias(xml.sax.ContentHandler):

    def __init__(self):
        super().__init__()
        self.in_categoria = False
        self.in_subcategoria = False
        self.categoria_nombre = []
        self.subcategoria_nombre = []
        #Guarda el nombre de la categoria para recordarla entre subcategorias
        self.categoria_actual = ""
        self.in_item = False
        self.listado_categorias = set()

    def startElement(self, name, attrs):

        if name.lower() == "categoria":
            self.in_categoria = True
        elif name.lower() == "subcategoria":
            self.in_subcategoria = True
        elif name.lower() == "item":
            label = attrs.get("name")
            if label.lower() == "categoria":
                self.in_item = True
                self.categoria_nombre = []
            elif label.lower() == "subcategoria":
                self.in_item = True
                self.subcategoria_nombre = []


    def characters(self, content):
        if self.in_categoria and not self.in_subcategoria and self.in_item:
            self.categoria_nombre.append(content)
        elif self.in_subcategoria and self.in_categoria and self.in_item:
            self.subcategoria_nombre.append(content)

    def endElement(self, name):

        if name.lower() == "item":
            if self.in_categoria and not self.in_subcategoria:
                self.categoria_actual = html.unescape("".join(self.categoria_nombre)).strip()
            self.in_item = False
        elif name.lower() == "categoria":
            self.in_categoria = False
        elif name.lower() == "subcategoria":
            string_return = self.categoria_actual + " > " + html.unescape("".join(self.subcategoria_nombre)).strip()
            self.listado_categorias.add(string_return)
            # print(f" '{self.categoria_actual} > {"".join(self.subcategoria_nombre)}' ")
            # Al encontrar que termina la subcategoria muestra todo
            # por pantalla directamente para que sea mas simple
            self.in_subcategoria = False


def subcategorias(filename):
    """Muestra todas todas las subcategorias de todos los restaurantes"""

    handler = _HandlerCategorias()
    xml.sax.parse(filename, handler)
    return handler.listado_categorias

#Ejercicio 3
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



#Ejercicio 4
def busqueda_cercania(filename, lugar, n):
    """"Devuelve una lista de restaurantes que esten 
    a menos de n km de lugar, ordenados de más cercano a más lejano"""

    arbol = ElementTree.parse(filename)

    localizador = Nominatim(user_agent="ej4")
    localizacion = localizador.geocode(lugar)#Buscamos el lugar utilizando nominatim
    if localizacion is None:
        # print("La calle no existe")
        return None

    datos = localizacion.raw#Saca los datos en formato json

    lat = datos["lat"]
    lon = datos["lon"]

    result_list = busqueda_cercania_aux(arbol, (lat, lon), n)

    # Cuando tenemos ya la lista completa la ordenamos para devolverla en base
    # al elemento 0 de la pareja p que es la distancia
    result_list.sort(key=lambda p: p[0])
    return result_list

def busqueda_cercania_aux(arbol,origen,max_dist):
    '''Returns the unoredered result list for busqueda_cercania'''
    result_list = []
    for element in arbol.iter("service"):
        nodo_nombre = element.find(".//name")#Busca la etiqueta name en todos los hijos del service
        if nodo_nombre is None:
            continue

        nombre_restaurante = html.unescape(nodo_nombre.text).strip()

        geo_data = element.find("geoData")
        if geo_data is None:
            continue

        latitud = geo_data.find("latitude")
        longitud = geo_data.find("longitude")
        if latitud is None or longitud is None:
            continue

        destino = (latitud.text, longitud.text)

        distancia = geodesic(origen, destino)

        if distancia.kilometers <= max_dist:
            result_list.append((distancia.kilometers, nombre_restaurante))#Añade al final
    return result_list
