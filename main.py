# 1. Conectar con la BBDD y recuperar la URL que se desea inspeccionar
# 2. Por oden se conecta con una URL y se busca el precio
# 3. Si se encuentra el precio se añade a un Google Sheets, sino se pondrá -
# 4. También se pondrá la fecha y la hora de la inspección

from app.db.functions_db import dicc_producto_url
from app.scraper import extract_price
from app.sheets import actualizar_precio, columna_fecha_hora, obtener_o_crear_hoja


def main():
    # Conectamos con la BBDD y extraemos la URL y el nombre del producto
    diccionario = dicc_producto_url()

    # Creamos o bien obtenemos la primera hoja del Google Sheet
    sheet1 = obtener_o_crear_hoja()
    columna_fecha_hora(sheet1)
    for id, dicc_id in diccionario.items():
        nombre = list(dicc_id.keys())[0]
        url = list(dicc_id.values())[0]
        # print("NOMBRE ", nombre)
        # print("URL ", url)
        precio = extract_price(str(url))
        
        # Actualizamos el precio en el Google Sheet
        actualizar_precio(id=id, sheet=sheet1, precio=precio, nombre=nombre, url=url)
    
    # Por si se ha mostrado, nos aseguramos de que la primera columna esté oculta
    sheet1.hide_columns(0, 1)
        

if __name__ == "__main__":
    main()