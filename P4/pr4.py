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

import sqlite3 as sq

def crear_bd(db_filename):
    conn = sq.connect(db_filename)
    conn.execute("PRAGMA foreign_keys = ON")
    
    cur = conn.cursor()
    cur.execute("CREATE TABLE datos_generales (ticker TEXT PRIMARY KEY, nombre TEXT, indice TEXT, pais TEXT)")
    cur.execute("CREATE TABLE semanales_IBEX35 (ticker TEXT, fecha TEXT, precio REAL, PRIMARy KEY(ticker,fecha),FOREIGN KEY(ticker) REFERENCES datos_generales(ticker))")
    cur.close()


def cargar_bd(db_filename, tab_datos, tab_ibex35):
    conn = sq.connect(db_filename)
    cur = conn.cursor()



def consulta1(db_filename, indice):
    ...


def consulta2(db_filename):
    ...


def consulta3(db_filename, limite):
    ...


def consulta4(db_filename, ticker):
    ...


if __name__ == "__main__":
    crear_bd("fichero.db")