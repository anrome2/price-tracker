import gspread
from gspread.exceptions import SpreadsheetNotFound, APIError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from app.config import EMAIL, ID_CARPETA, NOMBRE_SHEET

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
def obtener_o_crear_hoja():
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
            
            spreadsheet.sheet1.update(values=[['NOMBRE', 'URL']], range_name='A1:B1')
                
        except APIError as e:
            print(f"❌ Error crítico de la API de Google: {e}")
            return None

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

# EJECUCIÓN DE PRUEBA
if __name__ == "__main__":
    hoja = obtener_o_crear_hoja()
