"""
Asignatura: GIW
Práctica 1
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

# Ejercicio 1

def dimension(matriz):
    """
    Calcula la dimension de una matriz, comprobando primero si la longitud es mayor a 0 y 
    posteriormente comprueba que cada fila tenga las mismas columnas
    """
    if len(matriz) == 0 or matriz is None:
        return None
    filas = len(matriz)
    columnas = len(matriz[0])

    for fila in matriz:
        if len(fila) != columnas:
            return None

    return (filas, columnas)

def es_cuadrada(matriz):
    """
    Comprueba su la matriz es cuadrada si el numero de filas = columnas
    """
    tamanio = dimension(matriz)

    if tamanio is None:
        return False
    filas = tamanio[0]
    columnas = tamanio[1]

    if filas == columnas:
        return True
    return False

def es_simetrica(matriz):
    """Devuelve True si la matriz es valida y cuadrada
    y adiccionalmente para cada posición ij en la matriz
    el elemento en la posición ji es equivalente. 
    Devuelve False en cualquier otro caso."""

    if not es_cuadrada(matriz):
        return False

    # Will check:
    # - a b d
    # a - c e
    # b c - f
    # d e f -
    y = 1
    while y < len(matriz):
        x = 0
        while x < y:
            if matriz[x][y] != matriz[y][x]:
                return False
            x += 1
        y += 1

    return True


def multiplica_escalar(matriz, k):
    '''Multiplica todos los elementos de la matriz por un escalar.
    De tal forma que después de esta operación cada elemento ij de la matriz
    es ahora equivalente a k*ij
    Devuelve None si la matriz tiene dimensiones válidas y la dimensión de cada columna es igual'''
    if((dimension is None) or (k is None)):
        return None

    return_value = [[elem*k for elem in linea] for linea in matriz]

    return return_value


def suma(matriz1, matriz2):
    """
    Comprueba que las matrices estén bien formadas y tengan la misma
    dimensión, y suma sus elementos en una nueva matriz.
    """
    d1 = dimension(matriz1)
    d2 = dimension(matriz2)

    if d1 is None or d2 is None or d1 != d2:
        return None

    matriz3 = []

    for i, filai in enumerate(matriz1):
        fila = []

        for j, valor in enumerate(filai):
            resultado = valor + matriz2[i][j]
            fila.append(resultado)

        matriz3.append(fila)

    return matriz3


# Ejercicio 2
def validar(grafo):
    """mira si el grafo que recibe es valido en base a ciertos requisitos"""


    if grafo is None or not ("nodos" in grafo and "aristas" in grafo):
        return False

    #nodos no vacios y sin repetir
    nodos = set()
    lista_nodos = grafo.get("nodos")
    if len(lista_nodos)==0:
        return False
    for elem in lista_nodos:
        if not elem in nodos:
            nodos.add(elem)
        else:
            return False

    #n origen exactamente los de nodos
    copia_nodos = set(nodos)
    nodos_origen = grafo.get("aristas").keys()
    for elem in nodos_origen:
        if elem in nodos:
            copia_nodos.remove(elem)

    if not(nodos_origen==nodos and len(copia_nodos)==0):
        return False

    # n destino aparecen en nodos y no repetidos
    # Guarda los valores que vayan apareciendo en el set, si hay
    # uno nuevo que ya esta ahi es repetido por lo que no es valido
    # Ademas, comprueba que los nodos a los que apuntan existan tambien
    aparecidos = set()
    for lista in grafo.get("aristas").values():
        aparecidos.clear()
        for elem in lista:
            if elem in aparecidos or not elem in nodos:
                return False
            aparecidos.add(elem)

    return True

def grado_entrada(grafo, nodo):
    """Calcula el grado de entrada de un nodo en el grafo.
    Devuelve el numero de aristas que apuntan a ese nodo
    o -1 si el grafo no es válido o el nodo no existe"""
    if not validar(grafo) or nodo not in grafo["nodos"]:
        return -1

    num_entradas = 0
    for destinos in grafo["aristas"].values():
        if nodo in destinos:
            num_entradas += 1
    return num_entradas

def distancia(grafo, nodo):
    """Calcula las distancias mínimas desde un nodo a todos los demás en el grafo.
    Devuelve un diccionario {nodo: distancia}. Si un nodo no es alcanzable, distancia = -1.
    Si el grafo no es válido o el nodo no existe devuelve None."""

    if not validar(grafo) or nodo not in grafo["nodos"]:
        return None

    dist = {}  #diccionario vacío donde se irán guardando las parejas

    for nodo_actual in grafo["nodos"]:
        #indica por defecto que el nodo aún no ha sido visitado o no es alcanzable
        dist[nodo_actual] = -1

    dist[nodo] = 0 #la distancia de un nodo a sí mismo es 0
    cola = [nodo]

    while cola:
        actual = cola.pop(0)
        for vecino in grafo["aristas"][actual]:
            if dist[vecino] == -1:
                dist[vecino] = dist[actual] + 1
                cola.append(vecino)
    return dist


if __name__ == "__main__":
    print("--- EJERCICIO 1 ---")
    matriz_normal = [[1, 2, 3], [4, 5, 6]]
    matriz_cuadrada = [[1, 2], [3, 4]]
    matriz_mal_formada = [[1, 2], [3, 4, 5]]
    matriz_no_simetrica = [[1, 1, 3], [2,2,3], [3,3,3]]
    matriz_simetrica = [[1, 2, 3], [2,5,2], [3,2,3]]

    # Funciones implementadas
    print(f"Dimensión matriz_normal: {dimension(matriz_normal)}")
    print(f"Dimensión matriz_mal_formada: {dimension(matriz_mal_formada)}")
    print(f"Es cuadrada matriz_cuadrada: {es_cuadrada(matriz_cuadrada)}")
    print(f"Es cuadrada matriz_normal: {es_cuadrada(matriz_normal)}")

    print(f"Es simetrica matriz_simetrica: {es_simetrica(matriz_simetrica)}")
    print(f"Es simetrica matriz_no_simetrica: {es_simetrica(matriz_no_simetrica)}")
    print(f"Es simetrica matriz_normal: {es_simetrica(matriz_normal)}")

    print(f"Suma matriz_normal + matriz_normal: {suma(matriz_normal,matriz_normal)}")
    print(f"Multiplicación 2* matriz_normal: {multiplica_escalar(matriz_normal,2)}")

    print(f"Es simétrica: {es_simetrica(matriz_simetrica)}")
    print(f"Multiplica escalar x2: {multiplica_escalar(matriz_normal, 2)}")

    print("\n--- EJERCICIO 2 ---")
    # Grafo de prueba
    g = {"nodos": ["a", "b", "c", "d"],
      "aristas": {"a": ["a", "b", "c"],
                   "b": ["a", "c"],
                   "c": ["c"],
                   "d": ["c"]
                    }
        }
    # 1. Prueba desde a
    print("distancia(g, 'a'):", distancia(g, "a"))
    # 2. Prueba desde el nodo b
    print("distancia(g, 'b'):", distancia(g, "b"))
    # 3. Prueba desde el nodo d
    print("distancia(g, 'd'):", distancia(g, "d"))
    # 4. Prueba con un nodo que no existe
    print("distancia(g, 'Z'):", distancia(g, "Z"))
    # 5. prueba validar
    print(f"Es valida: {validar(g)}")
    #print(f"Es valida: {validar({"nodos" : [1,2], "aristas":{1:[2], 2:[2]}})}")
    #print(f"Es valida: {validar({"nodos" : [1,2], "aristas":{1:[2]}})}")
    #print(f"Es valida: {validar({"nodos" : [], "aristas":{}})}")
    #print(f"Es valida: {validar({"nodos" : [1,2], "aristas":{1:[2], 2: [2,2]}})}")
    #print(f"Es valida: {validar({"nodos" : [1,2], "aristas":{1:[], 2: []}})}")

    # 6. Prueba del grado de entrada
    #print("Grado entrada(g, 'a'):", grado_entrada(g, "a"))
    #print("Grado entrada(g, 'd'):", grado_entrada(g, "d"))
    #print("Grado entrada(g, 'Z'):", grado_entrada(g, "Z"))
    #print("Grado entrada({'nodos': [1,2], 'aristas': {1: [2]}}, '2'):",
     #     grado_entrada({"nodos": [1, 2], "aristas": {1: [2]}}, "2"))
