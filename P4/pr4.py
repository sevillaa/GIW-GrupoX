"""
Asignatura: GIW
Práctica 4
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

import csv
import sqlite3 as sq
from datetime import datetime

def crear_bd(db_filename):
    """
    Crea la base de datos con las tablas datos_generales y semanales_IBEX35.
    Configura las claves primarias y la clave foránea entre ambas tablas.
    Cierra el cursor y la conexión al terminar.
    """
    conn = sq.connect(db_filename)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS datos_generales (
                ticker TEXT PRIMARY KEY,
                nombre TEXT,
                indice TEXT,
                pais TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS semanales_IBEX35 (
                ticker TEXT,
                fecha TEXT,
                precio REAL,
                PRIMARY KEY (ticker, fecha),
                FOREIGN KEY (ticker) REFERENCES datos_generales(ticker)
            )
        """)
    finally:
        cur.close()
        conn.close()


def cargar_bd(db_filename, tab_datos, tab_ibex35):
    """
    Carga los datos de los dos ficheros CSV en la base de datos.
    Convierte las fechas al formato YYYY-MM-DD HH:MM.
    """
    conn = sq.connect(db_filename)
    cur = conn.cursor()

    try:
        conn.execute("PRAGMA foreign_keys = ON")

        with open(tab_datos, encoding="utf-8", newline="") as archivo:
            lector = csv.DictReader(archivo, delimiter=";")

            for fila in lector:
                cur.execute("""
                    INSERT INTO datos_generales (ticker, nombre, indice, pais)
                    VALUES (?, ?, ?, ?)
                """, (fila["ticker"], fila["nombre"], fila["indice"], fila["pais"]))

        with open(tab_ibex35, encoding="utf-8", newline="") as archivo:
            lector = csv.DictReader(archivo, delimiter=";")

            for fila in lector:
                fecha = datetime.strptime(fila["fecha"], "%d/%m/%Y %H:%M")
                fecha = fecha.strftime("%Y-%m-%d %H:%M")
                precio = float(fila["precio"])

                cur.execute("""
                    INSERT INTO semanales_IBEX35 (ticker, fecha, precio)
                    VALUES (?, ?, ?)
                """, (fila["ticker"], fecha, precio))

        conn.commit()

    finally:
        cur.close()
        conn.close()



def consulta1(db_filename, indice):
    '''Devuelve una lista de tuplas.
    Cada tupla contiene un ticker y el nombre asociado
    Solo se devolverán tuplas cuyo indice sea el dado en 'indice'
    Se devuelven en orden ascendente de ticker'''
    conn = sq.connect(db_filename)
    try:
        cur = conn.execute("SELECT ticker, nombre "
        "FROM datos_generales "
        "WHERE indice=? "
        "ORDER BY ticker", [indice])
        return list(cur.fetchall())
        #¿devolver directamente cur.fetchall()?  -> igual en 147 y 164
    finally:
        conn.close()


def consulta2(db_filename):
    """Devuelve una lista de tuplas (ticker, nombre, precio máximo)
    de las distintas acciones del IBEX35 según datos históricos
    ordenados por nombre ascendente"""
    con = sq.connect(db_filename)

    try:
        cur = con.execute(
            "SELECT s.ticker, g.nombre, MAX(s.precio) "
            "FROM semanales_IBEX35 s "
            "JOIN datos_generales g on s.ticker = g.ticker "
            "GROUP BY s.ticker, g.nombre "
            "ORDER BY g.nombre"
        )
        return cur.fetchall()
    finally:
        con.close()



def consulta3(db_filename, limite):
    """Devuelve una lista de tuplas (ticker, nombre, precio_promedio, diferencia).
    Solo incluye acciones cuyo precio promedio sea superior a 'limite'
    y ordenado por precio promedio descendente."""
    conn = sq.connect(db_filename)
    try:
        cur = conn.execute("""
            SELECT dg.ticker,
                   dg.nombre,
                   AVG(s.precio) AS precio_promedio,
                   (MAX(s.precio) - MIN(s.precio)) AS diferencia
            FROM datos_generales dg
            JOIN semanales_IBEX35 s ON dg.ticker = s.ticker
            GROUP BY dg.ticker, dg.nombre
            HAVING precio_promedio > ?
            ORDER BY precio_promedio DESC
        """, [limite])
        return list(cur.fetchall())
    finally:
        conn.close()


def consulta4(db_filename, ticker):
    """ Devuelve tuplas del historico del valor de las acciones asociadas al ticker de entrada
     ordenado de más reciente a más antiguo"""

    conn = sq.connect(db_filename)

    try:
        cur = conn.execute(""
        "SELECT ticker, date(fecha), precio "
        "FROM semanales_IBEX35 "
        "WHERE ticker = ? "
        "ORDER BY fecha DESC", [ticker])
        return list(cur.fetchall())
    finally:
        conn.close()