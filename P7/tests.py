"""
Enrique Martín <emartinm@ucm.es> 2026
Tests de unidad para comprobar el API REST sobre asignaturas.
ES IMPRESCINDIBLE QUE EL SERVIDOR FLASK ESTÉ EJECUTÁNDOSE ANTES DE LANZAR LOS TESTS

Lanzar TODOS los tests desde el terminal:
$ python -m unittest tests.TestREST

Lanzar un test concreto desde el terminal:
$ python -m unittest tests.TestREST.test_get_horario_inexistente
"""

import copy
import unittest

import requests

HOST = "http://127.0.0.1:5000"
TIMEOUT = 1

ASIGS = [
    {"nombre": "IA", "numero_alumnos": 35,
     "horario": [{"dia": "lunes", "hora_inicio": 10, "hora_final": 12}]},
    {"nombre": "SO", "numero_alumnos": 65,
     "horario": [{"dia": "martes", "hora_inicio": 9, "hora_final": 11},
                 {"dia": "viernes", "hora_inicio": 9, "hora_final": 10}]},
    {"nombre": "RED", "numero_alumnos": 50, "horario": []},
    {"nombre": "MDL", "numero_alumnos": 85,
     "horario": [{"dia": "jueves", "hora_inicio": 15, "hora_final": 17}]},
    {"nombre": "TC", "numero_alumnos": 95,
     "horario": [{"dia": "lunes", "hora_inicio": 18, "hora_final": 19},
                 {"dia": "martes", "hora_inicio": 18, "hora_final": 19},
                 {"dia": "jueves", "hora_inicio": 18, "hora_final": 19}]},
    {"nombre": "EDA", "numero_alumnos": 15,
     "horario": [{"dia": "miercoles", "hora_inicio": 11, "hora_final": 13}]},
    {"nombre": "PLG", "numero_alumnos": 0, "horario": []},
    {"nombre": "ISBC", "numero_alumnos": 18,
     "horario": [{"dia": "domingo", "hora_inicio": 9, "hora_final": 10}]},
    {"nombre": "TP", "numero_alumnos": 50,
     "horario": [{"dia": "viernes", "hora_inicio": 12, "hora_final": 14}]},
]

NUEVAS = [
    {"nombre": "NUEVA", "numero_alumnos": 33,
     "horario": [{"dia": "sabado", "hora_inicio": 9, "hora_final": 14}]},
    {"nombre": "SIN_HORARIO", "numero_alumnos": 7, "horario": []},
]

HORARIO_OK = {"dia": "lunes", "hora_inicio": 8, "hora_final": 10}

BAD_ASIGS = [
    {},
    [],
    "IA",
    {"nombre": "SO"},
    {"numero_alumnos": 45},
    {"horario": [HORARIO_OK]},
    {"nombre": "SO", "numero_alumnos": 45},
    {"nombre": "SO", "horario": [HORARIO_OK]},
    {"numero_alumnos": 45, "horario": [HORARIO_OK]},
    # Campos adicionales
    {"nombre": "RED", "numero_alumnos": 30, "horario": [HORARIO_OK], "creditos": 6},
    {"nombre": "RED", "numero_alumnos": 30, "horario": [HORARIO_OK], "id": 12},
    {"id": 8, "nombre": "RED", "numero_alumnos": 30},
    # Tipos incorrectos
    {"nombre": 42, "numero_alumnos": 30, "horario": [HORARIO_OK]},
    {"nombre": None, "numero_alumnos": 30, "horario": [HORARIO_OK]},
    {"nombre": {"texto": "RED"}, "numero_alumnos": 30, "horario": [HORARIO_OK]},
    {"nombre": "RED", "numero_alumnos": "treinta", "horario": [HORARIO_OK]},
    {"nombre": "RED", "numero_alumnos": "30", "horario": [HORARIO_OK]},
    {"nombre": "RED", "numero_alumnos": 30.5, "horario": [HORARIO_OK]},
    {"nombre": "RED", "numero_alumnos": False, "horario": [HORARIO_OK]},
    {"nombre": "RED", "numero_alumnos": None, "horario": [HORARIO_OK]},
    # Horario mal formado
    {"nombre": "MDL", "numero_alumnos": 25, "horario": "lunes"},
    {"nombre": "MDL", "numero_alumnos": 25, "horario": HORARIO_OK},
    {"nombre": "MDL", "numero_alumnos": 25, "horario": None},
    {"nombre": "MDL", "numero_alumnos": 25, "horario": [[8, 10]]},
    {"nombre": "MDL", "numero_alumnos": 25, "horario": [HORARIO_OK, "martes"]},
    {"nombre": "TC", "numero_alumnos": 70,
     "horario": [{"dia": ["lunes"], "hora_inicio": 8, "hora_final": 10}]},
    {"nombre": "TC", "numero_alumnos": 70,
     "horario": [{"dia": None, "hora_inicio": 8, "hora_final": 10}]},
    {"nombre": "TC", "numero_alumnos": 70,
     "horario": [{"dia": "lunes", "hora_inicio": "ocho", "hora_final": 10}]},
    {"nombre": "TC", "numero_alumnos": 70,
     "horario": [{"dia": "lunes", "hora_inicio": 8, "hora_final": ""}]},
    {"nombre": "TC", "numero_alumnos": 70,
     "horario": [{"dia": "lunes", "hora_inicio": 8, "hora_final": 10.5}]},
    {"nombre": "TC", "numero_alumnos": 70,
     "horario": [{"dia": "lunes", "hora_inicio": True, "hora_final": 10}]},
    {"nombre": "TC", "numero_alumnos": 70,
     "horario": [{"dia": "lunes", "hora_inicio": False, "hora_final": 10}]},
    {"nombre": "TC", "numero_alumnos": 70,
     "horario": [{"dia": "lunes", "hora_inicio": None, "hora_final": 10}]},
    {"nombre": "TC", "numero_alumnos": 70,
     "horario": [{"dias": "lunes", "hora_inicio": 8, "hora_final": 10}]},
    {"nombre": "TC", "numero_alumnos": 70,
     "horario": [{"hora_inicio": 8, "hora_final": 10}]},
    {"nombre": "TC", "numero_alumnos": 70,
     "horario": [{"dia": "lunes", "inicio": 8, "hora_final": 10}]},
    {"nombre": "TC", "numero_alumnos": 70,
     "horario": [{"dia": "lunes", "hora_final": 10}]},
    {"nombre": "TC", "numero_alumnos": 70,
     "horario": [{"dia": "lunes", "hora_inicio": 8, "final": 10}]},
    {"nombre": "TC", "numero_alumnos": 70,
     "horario": [{"dia": "lunes", "hora_inicio": 8}]},
    {"nombre": "TC", "numero_alumnos": 70,
     "horario": [{"dia": "lunes", "hora_inicio": 8, "hora_final": 10, "grupo": "A"}]},
    {"nombre": "TC", "numero_alumnos": 70,
     "horario": [HORARIO_OK, {"dia": "martes", "hora_final": 10}]},
]

PATCH = [
    {"nombre": "MODIFICADA"},
    {"numero_alumnos": 41},
    {"horario": [{"dia": "jueves", "hora_inicio": 12, "hora_final": 14}]},
    {"horario": []},
    {"numero_alumnos": 0},
    {"horario": [{"dia": "miercoles", "hora_inicio": 17, "hora_final": 18},
                 {"dia": "viernes", "hora_inicio": 17, "hora_final": 18}]},
]

BAD_PATCH = [
    {},
    [],
    "numero_alumnos",
    {"nombre": 12},
    {"nombre": None},
    {"numero_alumnos": "cuarenta"},
    {"numero_alumnos": 40.5},
    {"numero_alumnos": True},
    {"horario": "lunes"},
    {"horario": HORARIO_OK},
    {"horario": [None]},
    {"horario": [{"dia": "martes", "hora_final": 12}]},
    {"horario": [{"dia": "martes", "hora_inicio": "diez", "hora_final": 12}]},
    {"aula": "4"},
    {"id": 3},
    {"nombre": "IA", "horario": []},
    {"numero_alumnos": 3, "id": 3},
    {"nombre": "IA", "numero_alumnos": 3, "horario": []},
]

BAD_PARAMS = [
    "per_page=2",
    "page=2",
    "per_page=2&alumnos_gte=30",
    "page=2&alumnos_gte=30",
    "page=dos&per_page=2",
    "page=2&per_page=dos",
    "page=2&per_page=2.5",
    "page=2&per_page=",
    "alumnos_gte=treinta",
    "alumnos_gte=30.5",
    "alumnos_gte=",
    "orden=nombre",
    "page=2&per_page=2&orden=nombre",
    "alumnos_gte=30&orden=nombre",
]

# Umbrales de alumnos_gte: incluyen los valores exactos de ASIGS y sus vecinos
UMBRALES = [0, 1, 14, 15, 16, 49, 50, 51, 94, 95, 96, 999]
UMBRALES_PAGINADO = [0, 16, 50, 90, 200]
# Número de alumnos mayor que el de cualquier asignatura de ASIGS
ALUMNOS_PATCH = 700


def ruta(asig):
    """Ruta de una asignatura con identificador"""
    return f"/asignaturas/{asig['id']}"


def rutas_paginado(list_asignaturas, per_page, page):
    """Conjunto de rutas de la página 'page' con 'per_page' asignaturas por página"""
    return {ruta(a) for a in list_asignaturas[(page - 1) * per_page:page * per_page]}


class TestREST(unittest.TestCase):  # pylint: disable=too-many-public-methods
    """Tests a ejecutar sobre el servidor con el API REST"""

    @classmethod
    def setUpClass(cls):
        cls.s = requests.Session()

    @classmethod
    def tearDownClass(cls):
        cls.s.close()

    def borra_e_inserta(self, list_asignaturas):
        """Borra todas las asignaturas e inserta las de 'list_asignaturas' una por una.
        Devuelve una lista de asignaturas donde cada una ha sido extendida con su identificador"""
        r = self.s.delete(f'{HOST}/asignaturas', timeout=TIMEOUT)
        self.assertEqual(r.status_code, 204, "DELETE /asignaturas")
        added = []
        for asig in list_asignaturas:
            r = self.s.post(f'{HOST}/asignaturas', json=asig, timeout=TIMEOUT)
            self.assertEqual(r.status_code, 201, f"POST {asig}")
            self.assertEqual(list(r.json().keys()), ['id'], f"POST {asig}")
            new_asig = copy.deepcopy(asig)
            new_asig['id'] = r.json()['id']
            added.append(new_asig)
        return added

    def get_rutas(self, params=""):
        """Realiza GET /asignaturas?params, comprueba que devuelve 200 sin rutas
        repetidas y retorna el conjunto de rutas"""
        r = self.s.get(f'{HOST}/asignaturas?{params}', timeout=TIMEOUT)
        self.assertEqual(r.status_code, 200, f"GET /asignaturas?{params}")
        self.assertEqual(list(r.json().keys()), ['asignaturas'], f"GET /asignaturas?{params}")
        rutas = r.json()['asignaturas']
        self.assertEqual(len(rutas), len(set(rutas)), f"Rutas repetidas: {rutas}")
        return set(rutas)

    def assert_inexistente(self, ident):
        """Todas las operaciones sobre una asignatura inexistente devuelven 404"""
        url = f'{HOST}/asignaturas/{ident}'
        self.assertEqual(self.s.get(url, timeout=TIMEOUT).status_code, 404, f"GET {url}")
        self.assertEqual(self.s.get(f'{url}/horario', timeout=TIMEOUT).status_code, 404,
                         f"GET {url}/horario")
        self.assertEqual(self.s.put(url, json=NUEVAS[0], timeout=TIMEOUT).status_code, 404,
                         f"PUT {url}")
        self.assertEqual(self.s.patch(url, json=PATCH[0], timeout=TIMEOUT).status_code, 404,
                         f"PATCH {url}")
        self.assertEqual(self.s.delete(url, timeout=TIMEOUT).status_code, 404, f"DELETE {url}")

    # ---------- /asignaturas ----------

    def test_delete_asignaturas(self):
        """DELETE /asignaturas devuelve 204, también si ya no hay asignaturas"""
        for _ in range(2):
            r = self.s.delete(f'{HOST}/asignaturas', timeout=TIMEOUT)
            self.assertEqual(r.status_code, 204)

    def test_delete_get_asignaturas(self):
        """Tras borrar todas, GET devuelve una lista vacía y las antiguas no existen"""
        added = self.borra_e_inserta(ASIGS)
        self.borra_e_inserta([])
        self.assertEqual(self.get_rutas(), set())
        for asig in added:
            # subTest: si este caso falla, muestra sus datos y sigue con los demás
            with self.subTest(asig=asig):
                self.assert_inexistente(asig['id'])

    def test_post_identificadores(self):
        """POST devuelve {'id': N} con N natural, distinto y creciente"""
        for _ in range(2):
            ids = [a['id'] for a in self.borra_e_inserta(ASIGS)]
            for ident in ids:
                self.assertIs(type(ident), int, f"Identificador {ident!r} no es int")
                self.assertGreaterEqual(ident, 0)
            self.assertEqual(ids, sorted(set(ids)), f"Identificadores no crecientes: {ids}")

    def test_post_get_asignaturas(self):
        """GET devuelve las rutas a todas las asignaturas añadidas"""
        added = self.borra_e_inserta(ASIGS)
        self.assertEqual(self.get_rutas(), {ruta(a) for a in added})

    def test_post_incorrecto(self):
        """POST con asignaturas mal formadas devuelve 400 y no las añade"""
        added = self.borra_e_inserta(ASIGS)
        for asig in BAD_ASIGS:
            # subTest: si este caso falla, muestra sus datos y sigue con los demás
            with self.subTest(asig=asig):
                r = self.s.post(f'{HOST}/asignaturas', json=asig, timeout=TIMEOUT)
                self.assertEqual(r.status_code, 400)
        self.assertEqual(self.get_rutas(), {ruta(a) for a in added})

    def test_get_filtro(self):
        """GET con el parámetro alumnos_gte"""
        added = self.borra_e_inserta(ASIGS)
        for umbral in UMBRALES:
            # subTest: si este caso falla, muestra sus datos y sigue con los demás
            with self.subTest(alumnos_gte=umbral):
                expected = {ruta(a) for a in added if a['numero_alumnos'] >= umbral}
                self.assertEqual(self.get_rutas(f"alumnos_gte={umbral}"), expected)

    def test_get_paginado(self):
        """GET con los parámetros page y per_page, en cualquier orden"""
        added = self.borra_e_inserta(ASIGS)
        for per_page in range(1, len(ASIGS) + 2):
            for page in range(1, len(ASIGS) + 2):
                # subTest: si este caso falla, muestra sus datos y sigue con los demás
                with self.subTest(per_page=per_page, page=page):
                    expected = rutas_paginado(added, per_page, page)
                    self.assertEqual(self.get_rutas(f"per_page={per_page}&page={page}"),
                                     expected)
                    self.assertEqual(self.get_rutas(f"page={page}&per_page={per_page}"),
                                     expected)

    def test_get_paginado_filtro(self):
        """GET con los 3 parámetros: el paginado se aplica tras el filtrado"""
        added = self.borra_e_inserta(ASIGS)
        for umbral in UMBRALES_PAGINADO:
            filtradas = [a for a in added if a['numero_alumnos'] >= umbral]
            for per_page in range(1, 6):
                for page in range(1, 6):
                    # subTest: si este caso falla, muestra sus datos y sigue con los demás
                    with self.subTest(alumnos_gte=umbral, per_page=per_page, page=page):
                        rutas = self.get_rutas(
                            f"page={page}&alumnos_gte={umbral}&per_page={per_page}")
                        self.assertEqual(rutas, rutas_paginado(filtradas, per_page, page))

    def test_get_paginado_tras_borrado(self):
        """El paginado tiene en cuenta las asignaturas borradas"""
        added = self.borra_e_inserta(ASIGS)
        for asig in added[::2]:
            self.s.delete(f'{HOST}{ruta(asig)}', timeout=TIMEOUT)
        resto = added[1::2]
        for per_page in range(1, 4):
            for page in range(1, 4):
                # subTest: si este caso falla, muestra sus datos y sigue con los demás
                with self.subTest(per_page=per_page, page=page):
                    self.assertEqual(self.get_rutas(f"per_page={per_page}&page={page}"),
                                     rutas_paginado(resto, per_page, page))

    def test_get_parametros_incorrectos(self):
        """GET con parámetros incorrectos devuelve 400"""
        self.borra_e_inserta(ASIGS)
        for params in BAD_PARAMS:
            # subTest: si este caso falla, muestra sus datos y sigue con los demás
            with self.subTest(params=params):
                r = self.s.get(f'{HOST}/asignaturas?{params}', timeout=TIMEOUT)
                self.assertEqual(r.status_code, 400)

    def test_content_type_json(self):
        """Las respuestas con datos tienen Content-Type application/json"""
        asig = self.borra_e_inserta(ASIGS[:1])[0]
        respuestas = {
            "POST /asignaturas": self.s.post(f'{HOST}/asignaturas', json=ASIGS[0],
                                             timeout=TIMEOUT),
            "GET /asignaturas": self.s.get(f'{HOST}/asignaturas', timeout=TIMEOUT),
            "GET /asignaturas/X": self.s.get(f'{HOST}{ruta(asig)}', timeout=TIMEOUT),
            "GET /asignaturas/X/horario": self.s.get(f'{HOST}{ruta(asig)}/horario',
                                                     timeout=TIMEOUT),
        }
        for peticion, r in respuestas.items():
            # subTest: si este caso falla, muestra sus datos y sigue con los demás
            with self.subTest(peticion=peticion):
                self.assertTrue(r.headers['Content-Type'].startswith('application/json'))

    def test_post_sin_cuerpo(self):
        """POST sin cuerpo devuelve 400 y no añade ninguna asignatura"""
        self.borra_e_inserta([])
        r = self.s.post(f'{HOST}/asignaturas', timeout=TIMEOUT)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(len(self.get_rutas()), 0)

    # ---------- /asignaturas/X ----------

    def test_get_asignatura(self):
        """GET individual devuelve la asignatura con su identificador"""
        added = self.borra_e_inserta(ASIGS)
        for asig in added:
            # subTest: si este caso falla, muestra sus datos y sigue con los demás
            with self.subTest(asig=asig):
                r = self.s.get(f'{HOST}{ruta(asig)}', timeout=TIMEOUT)
                self.assertEqual(r.status_code, 200)
                self.assertEqual(r.json(), asig)

    def test_asignatura_inexistente(self):
        """GET, PUT, PATCH, DELETE y GET del horario sobre asignaturas inexistentes devuelven 404"""
        added = self.borra_e_inserta(ASIGS)
        max_id = max(a['id'] for a in added)
        for ident in range(max_id + 1, max_id + 6):
            # subTest: si este caso falla, muestra sus datos y sigue con los demás
            with self.subTest(ident=ident):
                self.assert_inexistente(ident)

    def test_delete_asignatura(self):
        """DELETE individual borra solo esa asignatura y deja de existir"""
        for i in range(len(ASIGS)):
            # subTest: si este caso falla, muestra sus datos y sigue con los demás
            with self.subTest(i=i):
                added = self.borra_e_inserta(ASIGS)
                borrada = added.pop(i)
                r = self.s.delete(f'{HOST}{ruta(borrada)}', timeout=TIMEOUT)
                self.assertEqual(r.status_code, 204)
                self.assertEqual(self.get_rutas(), {ruta(a) for a in added})
                self.assert_inexistente(borrada['id'])
                for asig in added:
                    r = self.s.get(f'{HOST}{ruta(asig)}', timeout=TIMEOUT)
                    self.assertEqual(r.json(), asig)

    def test_post_tras_delete_asignatura(self):
        """Tras borrar una asignatura, la siguiente no repite el identificador de otra existente"""
        added = self.borra_e_inserta(ASIGS)
        borrada = added.pop(0)
        self.s.delete(f'{HOST}{ruta(borrada)}', timeout=TIMEOUT)
        r = self.s.post(f'{HOST}/asignaturas', json=NUEVAS[0], timeout=TIMEOUT)
        self.assertEqual(r.status_code, 201)
        self.assertNotIn(r.json()['id'], [a['id'] for a in added])
        self.assertEqual(len(self.get_rutas()), len(ASIGS))

    def test_put_asignatura(self):
        """PUT reemplaza la asignatura conservando su identificador y sin modificar el resto"""
        added = self.borra_e_inserta(ASIGS)
        for i, asig in enumerate(added):
            for nueva in NUEVAS:
                # subTest: si este caso falla, muestra sus datos y sigue con los demás
                with self.subTest(asig=asig, nueva=nueva):
                    r = self.s.put(f'{HOST}{ruta(asig)}', json=nueva, timeout=TIMEOUT)
                    self.assertEqual(r.status_code, 200)
                    added[i] = {**nueva, 'id': asig['id']}
                    r = self.s.get(f'{HOST}{ruta(asig)}', timeout=TIMEOUT)
                    self.assertEqual(r.json(), added[i])
                    r = self.s.get(f'{HOST}{ruta(asig)}/horario', timeout=TIMEOUT)
                    self.assertEqual(r.json(), {'horario': nueva['horario']})
        self.assertEqual(self.get_rutas(), {ruta(a) for a in added})
        for asig in added:
            r = self.s.get(f'{HOST}{ruta(asig)}', timeout=TIMEOUT)
            self.assertEqual(r.json(), asig)

    def test_put_asignatura_mal_formada(self):
        """PUT con datos mal formados devuelve 404 si no existe y 400 si existe,
        sin modificar la asignatura"""
        added = self.borra_e_inserta(ASIGS[:3])
        max_id = max(a['id'] for a in added)
        for data in BAD_ASIGS:
            # subTest: si este caso falla, muestra sus datos y sigue con los demás
            with self.subTest(data=data):
                r = self.s.put(f'{HOST}/asignaturas/{max_id + 1}', json=data, timeout=TIMEOUT)
                self.assertEqual(r.status_code, 404)
        for asig in added:
            for data in BAD_ASIGS:
                # subTest: si este caso falla, muestra sus datos y sigue con los demás
                with self.subTest(asig=asig, data=data):
                    r = self.s.put(f'{HOST}{ruta(asig)}', json=data, timeout=TIMEOUT)
                    self.assertEqual(r.status_code, 400)
            r = self.s.get(f'{HOST}{ruta(asig)}', timeout=TIMEOUT)
            self.assertEqual(r.json(), asig)

    def test_patch_asignatura(self):
        """PATCH modifica únicamente el campo indicado"""
        added = self.borra_e_inserta(ASIGS)
        for asig in added:
            for patch in PATCH:
                # subTest: si este caso falla, muestra sus datos y sigue con los demás
                with self.subTest(asig=asig, patch=patch):
                    r = self.s.patch(f'{HOST}{ruta(asig)}', json=patch, timeout=TIMEOUT)
                    self.assertEqual(r.status_code, 200)
                    asig.update(patch)
                    r = self.s.get(f'{HOST}{ruta(asig)}', timeout=TIMEOUT)
                    self.assertEqual(r.json(), asig)
                    r = self.s.get(f'{HOST}{ruta(asig)}/horario', timeout=TIMEOUT)
                    self.assertEqual(r.json(), {'horario': asig['horario']})
        self.assertEqual(self.get_rutas(), {ruta(a) for a in added})

    def test_patch_filtro(self):
        """El filtro alumnos_gte tiene en cuenta los cambios realizados con PATCH"""
        added = self.borra_e_inserta(ASIGS)
        for asig in added[:4]:
            self.s.patch(f'{HOST}{ruta(asig)}', json={"numero_alumnos": ALUMNOS_PATCH},
                         timeout=TIMEOUT)
        self.assertEqual(self.get_rutas(f"alumnos_gte={ALUMNOS_PATCH}"),
                         {ruta(a) for a in added[:4]})

    def test_patch_asignatura_mal_formada(self):
        """PATCH con datos mal formados devuelve 404 si no existe y 400 si existe,
        sin modificar la asignatura"""
        added = self.borra_e_inserta(ASIGS[:3])
        max_id = max(a['id'] for a in added)
        for data in BAD_PATCH:
            # subTest: si este caso falla, muestra sus datos y sigue con los demás
            with self.subTest(data=data):
                r = self.s.patch(f'{HOST}/asignaturas/{max_id + 1}', json=data,
                                 timeout=TIMEOUT)
                self.assertEqual(r.status_code, 404)
        for asig in added:
            for data in BAD_PATCH:
                # subTest: si este caso falla, muestra sus datos y sigue con los demás
                with self.subTest(asig=asig, data=data):
                    r = self.s.patch(f'{HOST}{ruta(asig)}', json=data, timeout=TIMEOUT)
                    self.assertEqual(r.status_code, 400)
            r = self.s.get(f'{HOST}{ruta(asig)}', timeout=TIMEOUT)
            self.assertEqual(r.json(), asig)

    def test_put_patch_sin_cuerpo(self):
        """PUT y PATCH sin cuerpo devuelven 404 si la asignatura no existe y 400 si existe"""
        asig = self.borra_e_inserta(ASIGS[:1])[0]
        for metodo in [self.s.put, self.s.patch]:
            # subTest: si este caso falla, muestra sus datos y sigue con los demás
            with self.subTest(metodo=metodo.__name__.upper()):
                r = metodo(f'{HOST}/asignaturas/{asig["id"] + 1}', timeout=TIMEOUT)
                self.assertEqual(r.status_code, 404)
                r = metodo(f'{HOST}{ruta(asig)}', timeout=TIMEOUT)
                self.assertEqual(r.status_code, 400)
        r = self.s.get(f'{HOST}{ruta(asig)}', timeout=TIMEOUT)
        self.assertEqual(r.json(), asig)

    # ---------- /asignaturas/X/horario ----------

    def test_get_horario(self):
        """GET del horario devuelve un JSON con únicamente el campo 'horario'"""
        added = self.borra_e_inserta(ASIGS)
        for asig in added:
            # subTest: si este caso falla, muestra sus datos y sigue con los demás
            with self.subTest(asig=asig):
                r = self.s.get(f'{HOST}{ruta(asig)}/horario', timeout=TIMEOUT)
                self.assertEqual(r.status_code, 200)
                self.assertEqual(r.json(), {'horario': asig['horario']})

    def test_get_horario_inexistente(self):
        """GET del horario de una asignatura inexistente devuelve 404"""
        added = self.borra_e_inserta(ASIGS[:2])
        self.s.delete(f'{HOST}{ruta(added[0])}', timeout=TIMEOUT)
        for ident in [added[0]['id']] + list(range(added[1]['id'] + 1, added[1]['id'] + 6)):
            # subTest: si este caso falla, muestra sus datos y sigue con los demás
            with self.subTest(ident=ident):
                r = self.s.get(f'{HOST}/asignaturas/{ident}/horario', timeout=TIMEOUT)
                self.assertEqual(r.status_code, 404)
