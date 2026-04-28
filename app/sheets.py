from typing import Optional

import gspread
from datetime import datetime
from gspread.exceptions import SpreadsheetNotFound, APIError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from app.config import EMAIL, ID_CARPETA, NOMBRE_SHEET
from app.tools.auxiliar import numero_a_letra

# CREDENCIALES
def credenciales():
    # El 'scope' define qué permisos estamos pidiendo
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file"
    ]
    
    # Cargar las credenciales desde el archivo JSON
    flow = InstalledAppFlow.from_client_secrets_file(
        '.secrets/oauth_credentials.json', scope)
    creds = flow.run_local_server(port=0)
    return creds


# CONFIGURACIÓN DE CREDENCIALES
def conectar_google(creds):
    client = gspread.authorize(creds)
    return client

# LÓGICA DE CREACIÓN O APERTURA
def obtener_o_crear_hoja() -> gspread.Worksheet:
    creds = credenciales()
    gc = conectar_google(creds=creds)
      
    # 1. Intentamos abrir el archivo por nombre y el ID de la carpeta
    # Nota: Si hay varios con el mismo nombre, abrirá el más reciente         
    files = buscar_archivo_en_carpeta(creds=creds)

    spreadsheet = None
    for f in files:
        spreadsheet = gc.open_by_key(f['id'])
        print(f"✅ Archivo '{NOMBRE_SHEET}' encontrado y abierto.")
        break    
       
    # 2. Si no existe, procedemos a crearlo dentro de la carpeta específica
    if spreadsheet is None:
        print(f"⚠️ El archivo no existe. Creando '{NOMBRE_SHEET}' en la carpeta autorizada...")                  
        try:             
            # Creamos el archivo indicando el folder_id para usar TU cuota de espacio             
            spreadsheet = gc.create(NOMBRE_SHEET, folder_id=ID_CARPETA)                          
            # 3. Lo compartimos con tu email para que seas el dueño/editor visible             
            # # Aunque esté en tu carpeta, el "creador" técnico es el bot             
            spreadsheet.share(EMAIL, perm_type='user', role='writer')                          
            print(f"🚀 Archivo creado con éxito y compartido con {EMAIL}")
            
            spreadsheet.sheet1.update(values=[['ID', 'NOMBRE', 'URL']], range_name='A1:C1')

            # 2. Definir el rango a poner en negrita (ejemplo: A1:C1)
            rango = "A1:C1"

            # 3. Aplicar formato de negrita
            spreadsheet.sheet1.format(rango, {
                "backgroundColor": {
                    "red": 0.6,
                    "green": 0.6,
                    "blue": 1.0
                    },
                "textFormat": {
                    "bold": True
                }
            })
            # 4. Ocultar columna de ID
            spreadsheet.sheet1.hide_columns(0, 1)
                
        except APIError as e:
            print(f"❌ Error crítico de la API de Google: {e}")
            raise RuntimeError(f"No se pudo crear o abrir la hoja de cálculo: {e}") from e

    # Retornamos la primera hoja (tab) del archivo
    return spreadsheet.sheet1

def buscar_archivo_en_carpeta(creds):
    
    service = build('drive', 'v3', credentials=creds)

    query = f"""
        name = '{NOMBRE_SHEET}'
        and mimeType = 'application/vnd.google-apps.spreadsheet'
        and '{ID_CARPETA}' in parents
        and trashed = false
    """

    results = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)'
    ).execute()

    return results.get('files', [])

def columna_fecha_hora(sheet: gspread.Worksheet):
    # Nombre de la nueva columna, será la fecha y hora de la extracción del precio del producto
    # Extraemos la hora exacta de la consulta
    ts = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    # Número de columnas actuales
    # last_col = len(sheet.get_all_values()[0])
    # Para el formato necesitamos la letra que es
    # letra1 = numero_a_letra(last_col+1)

    # Insertamos el valor de la columna
    sheet.insert_cols([[ts]], 4)
    # Modificamos el formato, para el color de fondo, que sea negrita y el formato fecha y hora
    sheet.format(f"D1", {
        "numberFormat": {
            "type": "DATE_TIME",
            "pattern": "dd/mm/yyyy hh:mm:ss"
        },
        "backgroundColor": {
            "red": 0.6,
            "green": 0.6,
            "blue": 1.0
            },
        "textFormat": {
            "bold": True
        }
    })

def actualizar_precio(id: int, sheet: gspread.Worksheet, precio, nombre: str = "", url: str = ""):
    # En primer lugar buscamos si el id se encuentra en la columna 'ID'

    cell_list = sheet.findall(str(id), in_column=1)

    # Si no está el producto, se añade 
    if not cell_list:
        print(f"El producto {nombre} no está en el GS, añadiéndolo...")
        
        # Definimos los valores de la fila a insertar
        fila_datos = [str(id), nombre, f'=HYPERLINK("{url}"; "Enlace")', precio]
        last_row = len(sheet.get_all_values()) + 1
        sheet.insert_row(fila_datos, last_row, value_input_option="USER_ENTERED") # type: ignore
        
        # sheet.merge_cells(f"A{last_row}:A{last_row+1}")
        # sheet.merge_cells(f"B{last_row}:B{last_row+1}")
        # sheet.merge_cells(f"C{last_row}:C{last_row+1}")
    else:
        # Identificamos cuál es el índice de la fila
        row = cell_list[0].row
        # last_col = len(sheet.get_all_values()[0])
        sheet.update_cell(row, 4, precio)

def modificar_producto_sheet(id, nombre, url):
    sheet = obtener_o_crear_hoja()

    cell_list = sheet.findall(str(id), in_column=1)

    if not cell_list:
        print("El producto aún no se ha subido al Google Sheet, no hace falta modificarlo")
    else:
        row = cell_list[0].row
        if nombre:
            sheet.update_cell(row, 2, nombre)
        if url:
            sheet.update_cell(row, 3, f'=HYPERLINK("{url}", "Enlace")')

def mostrar_precios(id) -> list:
    sheet = obtener_o_crear_hoja()

    cell_list = sheet.findall(str(id), in_column=1)

    if not cell_list:
        print("El producto aún no se ha subido al Google Sheet, no hace falta modificarlo")
        return []
    else:
        row = cell_list[0].row
        # Las columnas que ocupa este producto
        n = sum(1 for cell in sheet.get_all_values()[row] if cell.strip())
        letra = numero_a_letra(n)

        listado_precios = sheet.get(f'D{row}:{letra}{row}')
        listado_fechas = sheet.get(f'D1:{letra}1')
        listado_fechas.append(listado_precios[0])
        return listado_fechas

# EJECUCIÓN DE PRUEBA
if __name__ == "__main__":
    hoja = obtener_o_crear_hoja()
