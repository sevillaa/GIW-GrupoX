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
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# APARTADO 1 #
def categorias():
    """ Devuelve un conjunto de parejas (nombre, número libros) de todas las categorías """
    res = requests.get(URL)
    s = set()
    try:
        res.raise_for_status()
        res.encoding = 'utf-8'
        html = res.text
        soup = BeautifulSoup(html, features="lxml")
        # The element that contains the list of categories
        # is the first <ul> element with no attributes inside
        mydivs = soup.find(ul_with_no_attrs)
        for a in mydivs.find_all("a"):
            s.add(explora_categoria(a.get("href")))
    except:
        print ("Hubo un problema")
    return s

def ul_with_no_attrs(tag):
    '''Returns true if tag name is ul and it has no attributes'''
    return tag.name == "ul" and not tag.attrs

def explora_categoria(url):
    '''Recibe la url desde una categoria categorias y extrae el nombre de la categoría y el número de ejemplares'''
    # print(url)
    if(url is None): 
        return
    category_url = urljoin(URL,url)
    res = requests.get(category_url)
    try:
        res.raise_for_status()
        res.encoding = 'utf-8'
        html = res.text
        soup = BeautifulSoup(html, features="lxml")
        name_tag = soup.select_one("div.page-header.action h1")
        number_tag = soup.select_one("form.form-horizontal strong")
        if name_tag is None or number_tag is None:
            return (None,None)
        name = name_tag.get_text(strip=True)
        elem_number = int(number_tag.get_text(strip=True))
        return (name, elem_number)
    except:
        print ("Hubo un problema")
        return (None,None)


# APARTADO 2 #
def libros_categoria(nombre):
    """ Dado el nombre de una categoría, devuelve un conjunto de tuplas 
        (titulo, precio, valoracion), donde el precio será un número real y la 
        valoración un número natural """
    ...

if __name__ == "__main__":
    print(categorias())