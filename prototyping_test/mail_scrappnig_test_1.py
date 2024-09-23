import imaplib
import email
from email.header import decode_header
import os

from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración del servidor y credenciales
IMAP_SERVER = 'imap.hostinger.com'
EMAIL_ACCOUNT = os.environ.get('EMAIL_ACCOUNT')
PASSWORD = os.environ.get('EMAIL_PASSWORD')

# Criterio de búsqueda: solo el remitente
REMITENTE_OBJETIVO = 'ldelgado@comce-soldicom.com'  # Reemplaza con el correo del remitente deseado

def clean(text):
    # Limpia el texto para usarlo en nombres de archivo
    return "".join(c if c.isalnum() else "_" for c in text)

def fetch_xls_from_mail(subfolder):
    # Verificar que las credenciales estén disponibles
    if not EMAIL_ACCOUNT or not PASSWORD:
        print("Error: Las credenciales de correo no están configuradas.")
        return

    try:
        # Conexión al servidor IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)

        # Autenticación
        mail.login(EMAIL_ACCOUNT, PASSWORD)

        # Seleccionar la bandeja de entrada
        mail.select('inbox')

        # Construir el criterio de búsqueda solo con el remitente
        criterio_busqueda = f'(FROM "{REMITENTE_OBJETIVO}")'

        # Buscar correos que coincidan con el criterio
        result, data = mail.search(None, criterio_busqueda)

        # Obtener la lista de IDs de correos
        email_ids = data[0].split()
        print(f'Correos encontrados: {len(email_ids)}')

        # Crear el directorio si no existe
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

        for email_id in email_ids:
            # Obtener el correo
            result, message_data = mail.fetch(email_id, '(RFC822)')
            raw_email = message_data[0][1]

            # Decodificar el correo
            email_message = email.message_from_bytes(raw_email)

            # Procesar los adjuntos
            for part in email_message.walk():
                # Si el mensaje es multipart
                if part.get_content_maintype() == 'multipart':
                    continue
                # Si es un adjunto
                if part.get('Content-Disposition') is None:
                    continue

                # Obtener el nombre del archivo adjunto
                filename = part.get_filename()
                if filename:
                    # Decodificar el nombre del archivo si es necesario
                    filename = decode_header(filename)[0][0]
                    if isinstance(filename, bytes):
                        filename = filename.decode('utf-8', errors='ignore')

                    # Verificar si el adjunto es un archivo de Excel
                    if filename.endswith(('.xls', '.xlsx')):
                        filepath = os.path.join(subfolder, clean(filename))
                        # Guardar el archivo adjunto
                        with open(filepath, 'wb') as f:
                            f.write(part.get_payload(decode=True))
                        print(f'Archivo guardado: {filepath}')

        # Cerrar la conexión
        mail.logout()

    except imaplib.IMAP4.error as e:
        print(f'Error al conectar o autenticar con el servidor IMAP: {e}')


# Especifica la subcarpeta donde se guardarán los archivos Excel
subfolder = 'encuestas_eds'  # Reemplaza con el nombre de la subcarpeta deseada
fetch_xls_from_mail(subfolder)
