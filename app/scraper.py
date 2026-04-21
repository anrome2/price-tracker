# Dada una URL, conectaremos con ella y trataremos de extraer el precio del producto
# Asumiremos que todas vienen de Amazon en un primer lugar
import urllib.robotparser
import requests
import time

from bs4 import BeautifulSoup

def check_permission(url):
    
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url("https://www.amazon.es/robots.txt")
    rp.read()

    # Miramos la ruta del producto o de precios
    puedo_mirar_precios = rp.can_fetch("MiScraperModelo", url=url)

    if puedo_mirar_precios:
        print("Legalmente puedo extraer el precio.")
        return True
    else:
        return False

def extract_price(url):
    # Dado que ya sabemos que la URL es válida, conectaremos con ella
    # Primero comprobamos si tenemos permiso:
    if check_permission(url=url):
        headers = {
            "User-Agent": "MiScraperModelo",
            "Accept-Language": "es-ES,es;q=0.9"
        }

        # Hacemos la petición de forma educada
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # 3. Analizar el HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 4. Buscar el precio. Buscamos por el ID directamente
            elemento_precio = soup.find('input', id='twister-plus-price-data-price')

            if elemento_precio:
                # Usamos ['value'] para sacar el contenido del atributo value
                precio_final = elemento_precio['value'] 
                print(f"Precio encontrado: {precio_final} €")
                return precio_final
            else:
                return None
        else:
            # Añadir reintentos
            print("No se pudo acceder a la página.")
            return None
    else:
        return None


if __name__ == "__main__":
    url = "https://www.amazon.es/Amazon-Basics-Espejos-longitud-completa/dp/B0DRCM73R2?ref_=ast_sto_dp&th=1"
    extract_price(url)