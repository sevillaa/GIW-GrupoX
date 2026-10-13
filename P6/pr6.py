"""
TODO: rellenar

Asignatura: GIW
Práctica 6
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

import requests

BASE_URL = 'http://127.0.0.1:8000/public/v2'
REST_TOKEN = 'local-dev-token-0001'



def inserta_usuarios(datos, token):
    """ Inserta todos los usuarios de la lista y devuelve el número de inserciones correctas """
    cont = 0
    for usuario in datos:
        response = requests.post(
            f"{BASE_URL}/users",
            headers={'Authorization' : f'Bearer {token}'},
            json=usuario,
            timeout=3#Timeout para que no se quede colgado si el servidor no responde
            )
        if response.status_code == 201:#Insercion correcta
            cont = cont+1
        elif response.status_code == 401:
            print("Token invalido")
    return cont


def get_ident_email(email, token):
    """ Devuelve el identificador del usuario cuyo email sea *exactamente* el pasado como parámetro.
        En caso de que ese usuario no exista devuelve None """
    response = requests.get(
        f"{BASE_URL}/users",
        headers={'Authorization' : f'Bearer {token}'},
        params={"email": email},
        timeout=3
        )
    if response.status_code == 200:#Codigo de que ha devuelto una lista (ejecucion correcta)
        for usuario in response.json():
            if usuario.get("email") == email:#Descarta los que contengan email como subcadena
                return usuario.get("id")
    elif response.status_code == 401:
        print("Token invalido")
    return None

def borra_usuario(email, token):
    """ Elimina el usuario cuyo email sea *exactamente* el pasado como parámetro. En caso de éxito en el
        borrado devuelve True. Si no existe tal usuario devolverá False """
    ...


def inserta_todo(email, token, title, due_on, status='pending'):
    """ Inserta un nuevo ToDo para el usuario con email exactamente igual al pasado. Si el ToDo ha sido insertado
        con éxito devolverá True, en otro caso devolverá False """
    ...


def todos_usuario(email, token):
    """ Devuelve una lista de diccionarios con todos los ToDo asociados al usuario con el email pasado como
        parámetro """
    ...


def todos_no_cumplidos(email, token):
    """ Devuelve una lista de diccionarios con todos los ToDo asociados al usuario con el email pasado como
        parámetro que están pendientes (status=pending) y cuya fecha tope (due_on) es anterior a la fecha
        y hora actual. Para comparar las fechas solo hay que tener en cuenta el dia, la hora y los minutos; es
        decir, ignorar los segundos, microsegundos y el uso horario """
    ...



if __name__  == "__main__":
    u1 = {'name': 'Eva', 'email': 'eva@gmail.com', 'gender': 'female', 'status': 'inactive'}
    u2 = {'name': 'Ana', 'email': 'ana@gmail.com', 'gender': 'female', 'status': 'active'}
    u3 = {'name': 'Pepe', 'email': 'pepe@gmail.com', 'gender': 'female', 'status': 'inactive'}
    print(inserta_usuarios([u1, u2], REST_TOKEN))
    print(inserta_usuarios([u3, u2], REST_TOKEN))
    print(get_ident_email('eva@gmail.com', REST_TOKEN))
    print(get_ident_email('barbara@gmail.com', REST_TOKEN))
