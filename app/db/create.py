import sqlite3

from app.config import DB_NAME, TABLE_DB_NAME

### CREAR LA BBDD
def crear_bbdd():
    # Creamos conexión con la BBDD
    conn = sqlite3.connect(DB_NAME)
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
    conn = sqlite3.connect(DB_NAME)
    # Creamos objeto cursor
    cursor = conn.cursor()
    # El ID será único por lo que tenemos que asignar un valor, será la numeración por orden de incorporación
    id_lista = cursor.execute(f'''SELECT ID FROM {TABLE_DB_NAME}''')
    # Buscamos el ID máximo, para que el nuevo valor tome el siguiente valor
    max_id = max(id_lista.fetchall())
    # Insertar una fila de datos
    cursor.execute(f'''INSERT INTO {TABLE_DB_NAME} VALUES ({max_id+1}, {nombre}, {url})''')
    # Guardamos cambios
    conn.commit()
    # Cerramos connexión con la BBDD
    conn.close()

### MODIFICAR UN CAMPO
def modificar_producto_bbdd(id: int, nombre: str = "", url: str = ""):
    # Creamos conexión con la BBDD
    conn = sqlite3.connect(DB_NAME)
    # Creamos objeto cursor
    cursor = conn.cursor()
    # Actualizamos el nombre o la url (o ambos) en caso de la que string no sea una cadena vacía
    if nombre:
        cursor.execute(f'''UPDATE {TABLE_DB_NAME} SET NOMBRE = {nombre} WHERE ID = {id}''')
    if url:
        cursor.execute(f'''UPDATE {TABLE_DB_NAME} SET URL = {url} WHERE ID = {id}''')
    # Guardamos cambios
    conn.commit()
    # Cerramos connexión con la BBDD
    conn.close()

### MOSTRAR LISTADO DE PRODUCTOS
def listado_productos_bbd():
    # Creamos conexión con la BBDD
    conn = sqlite3.connect(DB_NAME)
    # Creamos objeto cursor
    cursor = conn.cursor()
    # Seleccionamos el ID y NOMBRE para mostrarlo por pantalla
    res = cursor.execute(f'''SELECT ID, NOMBRE FROM {TABLE_DB_NAME}''')
    # Mostramos por pantalla todas las opciones disponibles
    for id, nombre in res:
        print(f"{id}. {nombre}\n")
    # Cerramos connexión con la BBDD
    conn.close()
