import gspread
from gspread.exceptions import SpreadsheetNotFound, APIError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

ID_CARPETA = "1SoGjTGcs56L_xJPdZjSfkBgRxJMB4Jjn"

# 1. CONFIGURACIÓN DE CREDENCIALES
def conectar_google():
    # El 'scope' define qué permisos estamos pidiendo
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file"
    ]
    
    # Cargar las credenciales desde el archivo JSON
    flow = InstalledAppFlow.from_client_secrets_file(
        '.secrets/oauth_credentials.json', scope)
    creds = flow.run_local_server(port=0)

    client = gspread.authorize(creds)
    return client

# 2. LÓGICA DE CREACIÓN O APERTURA
def obtener_o_crear_hoja(nombre_archivo, mi_email):
    gc = conectar_google()
    
    try:
        # 1. Intentamos abrir el archivo por nombre
        # Nota: Si hay varios con el mismo nombre, abrirá el más reciente
        spreadsheet = gc.open(nombre_archivo)
        print(f"✅ Archivo '{nombre_archivo}' encontrado y abierto.")
        
    except SpreadsheetNotFound:
        # 2. Si no existe, procedemos a crearlo dentro de la carpeta específica
        print(f"⚠️ El archivo no existe. Creando '{nombre_archivo}' en la carpeta autorizada...")
        
        try:
            # Creamos el archivo indicando el folder_id para usar TU cuota de espacio
            spreadsheet = gc.create(nombre_archivo, folder_id=ID_CARPETA)
            
            # 3. Lo compartimos con tu email para que seas el dueño/editor visible
            # Aunque esté en tu carpeta, el "creador" técnico es el bot
            spreadsheet.share(mi_email, perm_type='user', role='writer')
            
            print(f"🚀 Archivo creado con éxito y compartido con {mi_email}")
            
        except APIError as e:
            print(f"❌ Error crítico de la API de Google: {e}")
            return None
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado: {e}")
            return None

    # Retornamos la primera hoja (tab) del archivo
    return spreadsheet.sheet1

# 3. EJECUCIÓN
MI_EMAIL_PERSONAL = "andrxme2@gmail.com" # Cambia esto por tu cuenta real
nombre_del_sheet = "Price-Tracker"

hoja = obtener_o_crear_hoja(nombre_del_sheet, MI_EMAIL_PERSONAL)

# Prueba: Escribir algo en la primera fila
# hoja.update('A1', [['ID', 'Nombre', 'Fecha']])
# print("¡Proceso completado!")