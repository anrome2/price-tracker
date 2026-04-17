import os

from app.config import DB_NAME
from app.db.create import crear_bbdd, insertar_fila_bbdd, listado_productos_bbd, modificar_producto_bbdd


def main():
    # Al inicio le aparecerá al usuario un menú con 3 opciones para seleccionar:
    # 1. Añadir nuevo producto
    # 2. Modificar un campo existente de los productos almacenados en la BBDD
    # 3. Comprobar los precios de un producto
    accion = int(input("Escoja cuál de las siguientes acciones desea realizar, para ello introduzca el número que le corresponda del listado: \n"
                        "1. Añadir un nuevo producto\n" 
                        "2. Modificar un campo de los productos existentes almacenados en la BBDD \n"
                        "3. Comprobar los precios de un producto\n"
                        "Entrada: "))
    if accion == 1:
        print("Deberá introducir dos valores para poder registrarlo en la BBDD.")
        nombre = input("Nombre del producto: ")
        url = input("URL del producto: ")
        # Aquí comprobamos si existe la BBDD y sino la creamos
        if os.path.isfile(DB_NAME):
            print("La base de datos existe")
        else:
            print("La base de datos NO existe.Creándola...")
            crear_bbdd()
            print("Base de datos creada con éxito.")
        # Sabiendo que existe, insertamos los nuevos valores
        insertar_fila_bbdd()
        print(f"Insertado el producto {nombre} con éxito")
    elif accion == 2:
        print("Los productos existentes son:\n")
        # Aquí se printeará el listado de los productos almacenados en la BBDD existente
        print("Seleccione el producto que desea modificar. Mostrando productos disponibles...\n")
        # Llamamos a la función que los enumera
        listado_productos_bbd()
        id = int(input("Introduzca el número que corresponda al producto del listado citado: "))
        # Ahora se preguntará que desea modificar, si el nombre o la URL
        print(f"Del producto {id}, ¿qué desea modificar?")
        valor = int(input("1. El nombre del producto\n" \
        "2. La URL"))
        nombre = ""
        url = ""
        if valor == 1:
            nombre = input(f"Nuevo nombre del producto {id}: ")
        elif valor == 2:
            url = input(f"Nueva URL del producto {id}: ")
        else:
            print("Entrada errónea, vuelva a introducir un valor correcto entre 1-2")
        modificar_producto_bbdd(id=id, nombre=nombre, url=url)
        print(f"Modificado el producto {id} con éxito")
    elif accion == 3:
        print("Mostrando productos disponibles...\n")
        # Llamamos a la función que los enumera
        listado_productos_bbd()
        id = int(input("¿Cuál desea analizar? Introduzca el número que corresponda al producto del listado citado: "))
        # Aquí se mostrará un dataframe con los precios del producto almacenados
    else:
        print("Entrada errónea, vuelva a introducir un valor correcto entre 1-3")
    
if __name__ == "__main__":
    main()