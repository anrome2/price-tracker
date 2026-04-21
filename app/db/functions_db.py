import sqlite3

from app.config import DB_NAME, TABLE_DB_NAME

### CREAR LA BBDD
def crear_bbdd():
    # Creamos conexión con la BBDD
    # Por si la conexión falla, se puede controlar el error con un try except, pero en este caso se asume que la conexión se realiza correctamente
    try:
        conn = sqlite3.connect(DB_NAME)
    except sqlite3.Error as e:
        print(f"Error al conectar con la BBDD: {e}")
        return
    # Creamos objeto cursor
    cursor = conn.cursor()
    # Creamos tabla
    cursor.execute(f'''CREATE TABLE {TABLE_DB_NAME}
                   (ID int, NOMBRE text, URL text)
                   ''')
    # Guardamos cambios
    conn.commit()
    # Cerramos connexión con la BBDD
    conn.close()
    
### INSERTAR UNA FILA NUEVA
def insertar_fila_bbdd(nombre: str = "", url: str = ""):
    # Creamos conexión con la BBDD
    # Por si la conexión falla, se puede controlar el error con un try except, pero en este caso se asume que la conexión se realiza correctamente
    try:
        conn = sqlite3.connect(DB_NAME)
    except sqlite3.Error as e:
        print(f"Error al conectar con la BBDD: {e}")
        return
    # Creamos objeto cursor
    cursor = conn.cursor()
    # El ID será único por lo que tenemos que asignar un valor, será la numeración por orden de incorporación
    id_lista = cursor.execute(f'''SELECT ID FROM {TABLE_DB_NAME}''')
    rows = id_lista.fetchall()
    id_lista_mod = [x[0] for x in rows]
    # Buscamos el ID máximo, para que el nuevo valor tome el siguiente valor
    if id_lista_mod == []:
        # Si es la primera insercción estará vacío, asignar el 1
        max_id = 0
    else:
        max_id = max(id_lista_mod)
    # Insertar una fila de datos
    cursor.execute(f'''INSERT INTO {TABLE_DB_NAME} VALUES (?, ?, ?)''',
    (max_id + 1, nombre, url))
    # Guardamos cambios
    conn.commit()
    # Cerramos connexión con la BBDD
    conn.close()

### MODIFICAR UN CAMPO
def modificar_producto_bbdd(id: int, nombre: str = "", url: str = ""):
    # Creamos conexión con la BBDD
    # Por si la conexión falla, se puede controlar el error con un try except, pero en este caso se asume que la conexión se realiza correctamente
    try:
        conn = sqlite3.connect(DB_NAME)
    except sqlite3.Error as e:
        print(f"Error al conectar con la BBDD: {e}")
        return
    # Creamos objeto cursor
    cursor = conn.cursor()
    # Actualizamos el nombre o la url (o ambos) en caso de la que string no sea una cadena vacía
    if nombre:
        cursor.execute(
            f"UPDATE {TABLE_DB_NAME} SET NOMBRE = ? WHERE ID = ?",
            (nombre, id)
        )
    if url:
        cursor.execute(
                f"UPDATE {TABLE_DB_NAME} SET URL = ? WHERE ID = ?",
                (url, id)
            )
    # Guardamos cambios
    conn.commit()
    # Cerramos connexión con la BBDD
    conn.close()

### BUSCAR UN ID EN LA BBDD
def buscar_id_bbdd(id: int):
    # Creamos conexión con la BBDD
    # Por si la conexión falla, se puede controlar el error con un try except, pero en este caso se asume que la conexión se realiza correctamente
    try:
        conn = sqlite3.connect(DB_NAME)
    except sqlite3.Error as e:
        print(f"Error al conectar con la BBDD: {e}")
        return
    # Creamos objeto cursor
    cursor = conn.cursor()
    # Buscamos el ID en la columna
    res = cursor.execute(f'''SELECT NOMBRE FROM {TABLE_DB_NAME} WHERE ID = {id}''')
    if res.fetchone() is None:
        # Guardamos cambios
        conn.commit()
        # Cerramos connexión con la BBDD
        conn.close()
        return False
    else:
        # Guardamos cambios
        conn.commit()
        # Cerramos connexión con la BBDD
        conn.close()
        return True

### MOSTRAR LISTADO DE PRODUCTOS
def listado_productos_bbd():
    # Creamos conexión con la BBDD
    # Por si la conexión falla, se puede controlar el error con un try except, pero en este caso se asume que la conexión se realiza correctamente
    try:
        conn = sqlite3.connect(DB_NAME)
    except sqlite3.Error as e:
        print(f"Error al conectar con la BBDD: {e}")
        return
    # Creamos objeto cursor
    cursor = conn.cursor()
    # Seleccionamos el ID y NOMBRE para mostrarlo por pantalla
    res = cursor.execute(f'''SELECT ID, NOMBRE FROM {TABLE_DB_NAME}''')
    # Mostramos por pantalla todas las opciones disponibles
    for id, nombre in res:
        print(f"{id}. {nombre}\n")
    # Cerramos connexión con la BBDD
    conn.close()

### DEVUELVE DICCIONARIO PRODUCTO - URL
def dicc_producto_url():
    # Creamos conexión con la BBDD
    # Por si la conexión falla, se puede controlar el error con un try except, pero en este caso se asume que la conexión se realiza correctamente
    try:
        conn = sqlite3.connect(DB_NAME)
    except sqlite3.Error as e:
        print(f"Error al conectar con la BBDD: {e}")
        return {}
    # Creamos objeto cursor
    cursor = conn.cursor()
    # Seleccionamos el NOMBRE y URL
    res = cursor.execute(f'''SELECT ID, NOMBRE FROM {TABLE_DB_NAME}''')
    # Guardamos en un diccionario "producto": "url"
    diccionario = {}
    for nombre, url in res:
        diccionario[nombre] = url
    # Cerramos connexión con la BBDD
    conn.close()
    return diccionario