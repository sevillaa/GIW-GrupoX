"""
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

from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


URL = 'https://books.toscrape.com/'
TIMEOUT = 10


# APARTADO 1 #
def categorias():
    """ Devuelve un conjunto de parejas (nombre, número libros) de todas las categorías """
    res = requests.get(URL, timeout=TIMEOUT)
    s = set()

    res.raise_for_status()
    res.encoding = 'utf-8'
    html = res.text
    soup = BeautifulSoup(html, features="lxml")
    # The element that contains the list of categories
    # is the first <ul> element with no attributes inside
    mydivs = soup.find(ul_with_no_attrs)
    for a in mydivs.find_all("a"):
        s.add(explora_categoria(a.get("href")))

    return s

def ul_with_no_attrs(tag):
    '''Returns true if tag name is ul and it has no attributes'''
    return tag.name == "ul" and not tag.attrs

def explora_categoria(url):
    '''Recibe la url desde una categoria categorias y
    extrae el nombre de la categoría y el número de ejemplares'''
    # print(url)
    if url is None:
        return (None, None)
    category_url = urljoin(URL,url)
    res = requests.get(category_url, timeout=TIMEOUT)
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


# APARTADO 2 #
def url_categoria(nombre):
    """
    Devuelve la URL de la categoría, o None si no existe.
    Ignora espacios exteriores y diferencias entre mayúsculas y minúsculas.
    """
    nombre = nombre.strip().lower()
    res = requests.get(URL, timeout=TIMEOUT)
    res.raise_for_status()
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, features="lxml")

    for enlace in soup.select(".side_categories ul ul a"):
        if enlace.get_text(strip=True).lower() == nombre:
            return urljoin(URL, enlace["href"])
    return None


def libros_categoria(nombre):
    """
    Devuelve un conjunto de tuplas (titulo, precio, valoracion).
    Recorre todas las páginas de la categoría y devuelve títulos completos,
    precios float y valoraciones int. Si la categoría no existe, devuelve set().
    La búsqueda ignora espacios exteriores y diferencias de mayúsculas.
    """
    url = url_categoria(nombre)
    libros = set()
    valoraciones = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

    while url is not None:
        res = requests.get(url, timeout=TIMEOUT)
        res.raise_for_status()
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, features="lxml")

        for libro in soup.select("article.product_pod"):
            # El texto visible puede estar recortado, pero title contiene el completo.
            titulo = libro.select_one("h3 a")["title"]
            precio = float(libro.select_one("p.price_color").get_text(strip=True)
                           .removeprefix("£"))
            clases = libro.select_one("p.star-rating")["class"]
            valoracion = next(valoraciones[clase] for clase in clases
                              if clase in valoraciones)
            libros.add((titulo, precio, valoracion))

        siguiente = soup.select_one("li.next a")
        # Cada enlace next es relativo a la página que acabamos de leer.
        url = urljoin(url, siguiente["href"]) if siguiente is not None else None

    return libros
