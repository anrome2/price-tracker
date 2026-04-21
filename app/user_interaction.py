import os
import validators # Librería para validar las url

from .config import DB_NAME
from .db.functions_db import buscar_id_bbdd, crear_bbdd, insertar_fila_bbdd, listado_productos_bbd, modificar_producto_bbdd

def usr_interact():
    # Al inicio le aparecerá al usuario un menú con 3 opciones para seleccionar:
    # 1. Añadir nuevo producto
    # 2. Modificar un campo existente de los productos almacenados en la BBDD
    # 3. Comprobar los precios de un producto

    while True:
        try:
            accion = int(input("Escoja cuál de las siguientes acciones desea realizar, para ello introduzca el número que le corresponda del listado: \n"
                                "1. Añadir un nuevo producto\n" 
                                "2. Modificar un campo de los productos existentes almacenados en la BBDD \n"
                                "3. Comprobar los precios de un producto\n"
                                "Entrada: "))
            if accion == 1:
                print("Ha seleccionado añadir un nuevo producto. Deberá introducir el nombre del producto y su url para poder registrarlo en la BBDD.")
                # Comprobamos que los inputs sean correctos
                while True:
                    try:
                        nombre = str(input("Nombre del producto: "))
                        break  # si todo va bien, salimos del bucle
                    except ValueError:
                        print("El nombre debe ser una cadena de texto. Inténtalo de nuevo.")
                    
                while True:
                    try:
                        url = input("URL del producto: ")
                        if validators.url(url):
                            print("URL válida.") # Pasar a logger
                            break  # si todo va bien, salimos del bucle
                        else:
                            print("URL inválida.") # Pasar a logger
                        
                    except ValueError:
                        print("No es una URL válida. Inténtalo de nuevo.")
                    
                # Aquí comprobamos si existe la BBDD y sino la creamos
                if os.path.isfile(DB_NAME):
                    print("La base de datos existe")
                else:
                    print("La base de datos NO existe.Creándola...")
                    crear_bbdd()
                    print("Base de datos creada con éxito.")
                # Sabiendo que existe, insertamos los nuevos valores
                insertar_fila_bbdd(nombre=nombre, url=url)
                print(f"Insertado el producto {nombre} con éxito\n")
                print("¿Desea realizar alguna otra acción?\n")
                while True:
                    try:
                        valor = int(input("1. Si\n" \
                                "2. No\n"))
                        if valor == 1:
                            usr_interact()
                            break  # si todo va bien, salimos del bucle
                        elif valor == 2:
                            print("Saliendo...")
                            break
                        else:
                            print("El valor está fuera del rango disponible. Inténtalo de nuevo.")
                    except ValueError:
                        print("No es un número válido. Inténtalo de nuevo.")
                break
            elif accion == 2:
                print("Ha seleccionado modificar uno de los productos existentes.")
                # Aquí se printeará el listado de los productos almacenados en la BBDD existente
                print("Seleccione el producto que desea modificar. Mostrando productos disponibles...\n")
                # Llamamos a la función que los enumera
                listado_productos_bbd()
                while True:
                    try:
                        id = int(input("Introduzca el número que corresponda al producto del listado citado: "))
                        # Además de que sea int, deberá ser una de los IDs almacenados en la BBDD
                        correct_id = buscar_id_bbdd(id=id)
                        if correct_id:
                            break  # si todo va bien, salimos del bucle
                        else:
                            print("El valor está fuera del rango disponible. Inténtalo de nuevo.")
                    except ValueError:
                        print("No es un número válido. Inténtalo de nuevo.")
                # Ahora se preguntará que desea modificar, si el nombre o la URL
                print(f"Del producto {id}, ¿qué desea modificar?")
                while True:
                    try:
                        valor = int(input("1. El nombre del producto\n" \
                                "2. La URL\n"))
                        if valor in [1, 2]:
                            break  # si todo va bien, salimos del bucle
                        else:
                            print("El valor está fuera del rango disponible. Inténtalo de nuevo.")
                    except ValueError:
                        print("No es un número válido. Inténtalo de nuevo.")
                nombre = ""
                url = ""
                if valor == 1:  
                    while True:
                        try:
                            nombre = str(input(f"Nuevo nombre del producto {id}: "))
                            break  # si todo va bien, salimos del bucle
                        except ValueError:
                            print("El nombre debe ser una cadena de texto. Inténtalo de nuevo.")
                elif valor == 2:
                    while True:
                        try:
                            url = input(f"Nueva URL del producto {id}: ")
                            if validators.url(url):
                                print("URL válida.") # Pasar a logger
                                break  # si todo va bien, salimos del bucle
                            else:
                                print("URL inválida.") # Pasar a logger
                        except ValueError:
                            print("No es una URL válida. Inténtalo de nuevo.")
                
                modificar_producto_bbdd(id=id, nombre=nombre, url=url)
                print(f"Modificado el producto {id} con éxito")
                print("¿Desea realizar alguna otra acción?\n")
                while True:
                    try:
                        valor = int(input("1. Si\n" \
                                "2. No\n"))
                        if valor == 1:
                            usr_interact()
                            break  # si todo va bien, salimos del bucle
                        elif valor == 2:
                            print("Saliendo...")
                            break
                        else:
                            print("El valor está fuera del rango disponible. Inténtalo de nuevo.")
                    except ValueError:
                        print("No es un número válido. Inténtalo de nuevo.")
                break
            elif accion == 3:
                print("Ha seleccionado comprobar los precios de un producto. Mostrando productos disponibles...\n")
                # Llamamos a la función que los enumera
                listado_productos_bbd()
                while True:
                    try:
                        id = int(input("¿Cuál desea analizar? Introduzca el número que corresponda al producto del listado citado: "))
                        # Además de que sea int, deberá ser una de los IDs almacenados en la BBDD
                        correct_id = buscar_id_bbdd(id=id)
                        if correct_id:
                            break  # si todo va bien, salimos del bucle
                        else:
                            print("El valor está fuera del rango disponible. Inténtalo de nuevo.")
                    except ValueError:
                        print("No es un número válido. Inténtalo de nuevo.")
                # Aquí se mostrará un dataframe con los precios del producto almacenados
                print("¿Desea realizar alguna otra acción?\n")
                while True:
                    try:
                        valor = int(input("1. Si\n" \
                                "2. No\n"))
                        if valor == 1:
                            usr_interact()
                            break  # si todo va bien, salimos del bucle
                        elif valor == 2:
                            print("Saliendo...")
                            break
                        else:
                            print("El valor está fuera del rango disponible. Inténtalo de nuevo.")
                    except ValueError:
                        print("No es un número válido. Inténtalo de nuevo.")
                break
            else:
                print("Número fuera de rango, vuelva a introducir un valor entre 1-3")
        except ValueError:
                        print("No es un número válido. Inténtalo de nuevo.")
    
if __name__ == "__main__":
    usr_interact()