"""
TODO: rellenar

Asignatura: GIW
Práctica 8
Grupo: 10
Autores: Miguel Sevilla Benito, Izan de Vega López,
            Adrián Muñoz Rodríguez, Israel Suárez Fraile, Oier Osorio Illarramendi

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás
"""
import re
import math
from datetime import datetime

from mongoengine import (
    connect, Document, EmbeddedDocument,
    StringField, IntField, EmbeddedDocumentListField,
    ListField, ReferenceField, FloatField, ValidationError,
    PULL
    )

LETRAS_DNI = "TRWAGMYFPDXBNJZSQVHLCKE"

class Tarjeta(EmbeddedDocument):
    """Datos de tarjeta"""
    nombre = StringField(required = True, min_length=2)
    numero = StringField(required = True, regex= r"^\d{16}$")
    mes = StringField(required = True, regex=r"^(0[1-9]|1[0-2])$", max_length=2)
    year = StringField(required = True, regex=r"^\d{2}$")
    cvv = StringField(required = True, regex=r"^\d{3}$")

class Producto(Document):
    """Informacion de un producto"""
    codigo_barras = StringField(required = True, unique = True, regex=r"^\d{13}$")
    nombre = StringField(required = True, min_length=2)
    categoria_principal = IntField(required = True, min_value=0)
    categorias_secundarias = ListField(IntField(min_value=0))

    def clean(self):
        super().clean()

        if not isinstance(self.codigo_barras, str):
            return

        if len(self.codigo_barras)!=13:
            raise ValidationError(
                "El codigo de barras debe tener una longitud de 13"
            )

        num = self.codigo_barras[:12]
        cont = 1
        suma = 0
        for m in num:
            try:
                n = int(m)
            except Exception as exc:
                raise ValidationError(
                    "El codigo de barras debe ser representado con enteros"
                ) from exc

            if cont%2==0:
                suma = suma + n*3
            else:
                suma = suma + n
            cont+=1

        ultimo = (10 - (suma%10))%10

        try:
            control = int(self.codigo_barras[12])
        except Exception as exc:
            raise ValidationError(
                "El codigo de barras debe ser exclusivamente int"
            ) from exc
        if ultimo != control:
            raise ValidationError(
                "El ultimo digito no es correcto para el codigo de barras"
                )

        if (self.categorias_secundarias and
            self.categoria_principal != self.categorias_secundarias[0]):
            raise ValidationError(
                "La categoria principal debe aparecer " \
                "la primera en la lista de categorias secundarias"
            )


class Linea(EmbeddedDocument):
    """Datos de linea de pedido"""
    num_items = IntField(required = True, min_value=1)
    precio_item = FloatField(required = True, min_value=0.0)
    nombre_item = StringField(required = True, min_length=2)
    total = FloatField(required = True, min_value=0.0)
    producto = ReferenceField(Producto, required = True)

    def clean(self):
        super().clean()
  
        if (self.num_items is None or self.precio_item is None or self.total is None or self.producto is None or self.nombre_item is None):
            return

        numeros = (self.num_items, self.precio_item, self.total)
        if not all(isinstance(n, (int, float)) for n in numeros):
            return
                    
        if self.precio_item <= 0 or self.total <= 0:
            raise ValidationError("Los precios deben ser números reales positivos")

        if not math.isclose(self.num_items * self.precio_item, self.total):
            raise ValidationError(
                "El total de la línea no es num_items * precio_item"
            )

        if self.nombre_item != self.producto.nombre:
            raise ValidationError(
                "El nombre del producto en la linea y en la info del producto no coinciden"
            )


class Pedido(Document):
    """Estructura de pedido"""
    total = FloatField(required = True, min_value=0.0)
    fecha = StringField(required = True, regex=r"^\d{4},"#year
                        "(0[1-9]|1[0-2]),(0[1-9]|1[0-9]|2[0-9]|3[0-1]),"#mes, dia
                        "(0[0-9]|1[0-9]|2[0-3]),[0-5][0-9],"#hora,min,seg,
                        "[0-5][0-9],[0-9]{6}$")#nanoseg
    lineas = EmbeddedDocumentListField(Linea, required = True)

    

    def clean(self):
        super().clean()
                
        if (not isinstance(self.total, (int, float)) or
                not isinstance(self.fecha, str) or self.lineas is None):
            return

        if not isinstance(self.lineas, list):
            raise ValidationError(
                "El campo lineas debe ser una lista"
            )
                    
        if not self.lineas:
            raise ValidationError("El pedido debe tener al menos una línea")

        try:
            datetime.strptime(self.fecha, "%Y,%m,%d,%H,%M,%S,%f")
        except ValueError as exc:
            raise ValidationError("La fecha del pedido no existe en el calendario") from exc
                    
        suma_lineas = 0
        codigo_productos = set()

        for l in self.lineas:

            if not isinstance(l, Linea):
                raise ValidationError(
                    "Todos los elementos deben ser lineas"
                )
            if l.producto is None or l.total is None:
                raise ValidationError("Todas las lineas necesitan producto y total")

            suma_lineas = suma_lineas+l.total

            if l.producto.codigo_barras in codigo_productos:
                raise ValidationError("El pedido tiene dos lineas con el mismo producto")

            codigo_productos.add(l.producto.codigo_barras)

        if not math.isclose(suma_lineas, self.total):
            raise ValidationError("El pedido tiene un precio distinto al de la suma de sus lineas")



class Usuario(Document):
    """Estructura de un usuario"""
    dni = StringField(
        required = True, min_length= 9, max_length= 9,
        regex=r"^\d{8}[A-Z]{1}$", unique= True
        )
    nombre = StringField(required = True, min_length=2)
    apellido1 = StringField(required = True, min_length=2)
    apellido2 = StringField(min_length=2)
    #El enunciado solo dice que es opcional pero entiendo que sigue el formato de apellido1
    f_nac = StringField(
        required = True,
        regex=r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1])$"
        )
    tarjetas = EmbeddedDocumentListField(Tarjeta)
    pedidos = ListField(ReferenceField(Pedido, reverse_delete_rule=PULL))

    def clean(self):
        super().clean()

        if not isinstance(self.dni, str) or not isinstance(self.f_nac, str):
            return
        if not re.fullmatch(r"\d{8}[A-Z]", self.dni):
            raise ValidationError("El DNI debe tener 8 numeros y una letra")
                    
        try:
            datetime.strptime(self.f_nac, "%Y-%m-%d")
        except ValueError as exc:
            raise ValidationError("La fecha de nacimiento no existe en el calendario") from exc
                    
        num_dni = self.dni[:8]
        letra_dni = self.dni[8]
        numero = int(num_dni)
        resto = numero%23

        if letra_dni != LETRAS_DNI[resto]:
            raise ValidationError("La letra no es correcta para el numero del DNI")

if __name__ == "__main__":
    connect("giw_mongoengine")
