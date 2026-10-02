"""
TODO: rellenar

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
    finally:
        conn.close()


def consulta2(db_filename):
    ...


def consulta3(db_filename, limite):
    ...


def consulta4(db_filename, ticker):
    ...


if __name__ == "__main__":
    database_name ="database.sqlite3"
    crear_bd(database_name)
    cargar_bd(database_name, "Tabla1.csv","Tabla2.csv")
    print(consulta1(database_name,"Nasdaq 100"))
