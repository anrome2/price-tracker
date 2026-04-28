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
    # Primero comprobamos si tenemos permiso:
    if check_permission(url=url):
        headers = {
            "User-Agent": "MiScraperModelo",
            "Accept-Language": "es-ES,es;q=0.9"
        }

        # Hacemos la petición de forma educada
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # --- ESTRATEGIA 1: Input oculto (El más preciso) ---
                elemento_precio = soup.find('input', id='twister-plus-price-data-price')
                if elemento_precio and elemento_precio.get('value'):
                    precio_final = elemento_precio['value']
                    print(f"Precio encontrado (vía input): {precio_final} €")
                    return precio_final

                # --- ESTRATEGIA 2: Selector visual principal (apex-pricetopay) ---
                # Usamos el span que contiene el precio completo para evitar decimales separados
                contenedor_visual = soup.find('span', class_='apex-pricetopay-value')
                if contenedor_visual:
                    span_offscreen = contenedor_visual.find('span', class_='a-offscreen')
                    if span_offscreen:
                        precio_texto = span_offscreen.get_text(strip=True)
                        # Limpiamos: "29,99€" -> "29.99"
                        precio_final = precio_texto.replace('€', '').replace(',', '.').strip()
                        print(f"Precio encontrado (vía visual): {precio_final} €")
                        return precio_final

                # --- ESTRATEGIA 3: Selector genérico de Amazon (a-price) ---
                # Como última opción buscamos la clase estándar
                # etiqueta_a_price = soup.find('span', class_='a-price')
                # if etiqueta_a_price:
                #     span_invisible = etiqueta_a_price.find('span', class_='a-offscreen')
                #     if span_invisible:
                #         precio_texto = span_invisible.get_text(strip=True)
                #         precio_final = precio_texto.replace('€', '').replace(',', '.').strip()
                #         print(f"Precio encontrado (vía genérica): {precio_final} €")
                #         return precio_final

                print("No se encontró el selector de precio en esta página.")
                return None
            
            else:
                print(f"No se pudo acceder. Código de estado: {response.status_code}")
                return None
        
        except Exception as e:
            print(f"Error durante la petición: {e}")
            return None
    else:
        print("Permiso denegado por robots.txt")
        return None


if __name__ == "__main__":
    url = "https://www.amazon.es/Amazon-Basics-Espejos-longitud-completa/dp/B0DRCM73R2?ref_=ast_sto_dp&th=1"
    extract_price(url)