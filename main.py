# 1. Conectar con la BBDD y recuperar la URL que se desea inspeccionar
# 2. Por oden se conecta con una URL y se busca el precio
# 3. Si se encuentra el precio se añade a un Google Sheets, sino se pondrá -
# 4. También se pondrá la fecha y la hora de la inspección

from datetime import datetime

from app.db.functions_db import dicc_producto_url
from app.scraper import extract_price


def main():
    # Conectamos con la BBDD y extraemos la URL y el nombre del producto
    diccionario = dicc_producto_url()

    for nombre, url in diccionario.items():
        precio = extract_price(str(url))
        # Extraemos la hora exacta de la consulta
        ts = datetime.now().timestamp()

if __name__ == "__main__":
    main()