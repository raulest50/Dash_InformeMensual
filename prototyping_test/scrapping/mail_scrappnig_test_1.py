import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Server configuration and credentials
IMAP_SERVER = 'imap.hostinger.com'
EMAIL_ACCOUNT = os.environ.get('EMAIL_ACCOUNT')
PASSWORD = os.environ.get('EMAIL_PASSWORD')

# Search criterion: only the sender
REMITENTE_OBJETIVO = 'ldelgado@comce-soldicom.com'  # Replace with the desired sender's email

def clean(text):
    # Clean the text for use in filenames
    allowed_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._- ")
    return "".join(c if c in allowed_chars else "_" for c in text)

def fetch_xls_from_mail(subfolder):
    # Verify that credentials are available
    if not EMAIL_ACCOUNT or not PASSWORD:
        print("Error: Email credentials are not configured.")
        return

    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)

        # Authentication
        mail.login(EMAIL_ACCOUNT, PASSWORD)

        # Select the inbox
        mail.select('inbox')

        # Build the search criterion using only the sender
        criterio_busqueda = f'(FROM "{REMITENTE_OBJETIVO}")'

        # Search for emails matching the criterion
        result, data = mail.search(None, criterio_busqueda)

        # Get the list of email IDs
        email_ids = data[0].split()
        print(f'Correos encontrados: {len(email_ids)}')

        # Create the directory if it doesn't exist
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

        for email_id in email_ids:
            # Retrieve the email
            result, message_data = mail.fetch(email_id, '(RFC822)')
            raw_email = message_data[0][1]

            # Decode the email
            email_message = email.message_from_bytes(raw_email)

            # Process attachments
            for part in email_message.walk():
                # Skip multipart messages
                if part.get_content_maintype() == 'multipart':
                    continue
                # Skip if not an attachment
                if part.get('Content-Disposition') is None:
                    continue

                # Get the attachment's filename
                filename = part.get_filename()
                if filename:
                    # Decode the filename if necessary
                    filename = decode_header(filename)[0][0]
                    if isinstance(filename, bytes):
                        filename = filename.decode('utf-8', errors='ignore')

                    # Check if the attachment is an Excel file
                    if filename.endswith(('.xls', '.xlsx')):
                        # Clean the filename
                        filename = clean(filename)
                        filepath = os.path.join(subfolder, filename)
                        # Save the attachment
                        with open(filepath, 'wb') as f:
                            f.write(part.get_payload(decode=True))
                        print(f'Archivo guardado: {filepath}')

        # Close the connection
        mail.logout()

    except imaplib.IMAP4.error as e:
        print(f'Error al conectar o autenticar con el servidor IMAP: {e}')

# Specify the subfolder where Excel files will be saved
subfolder = 'encuestas_eds'  # Replace with the desired subfolder name
fetch_xls_from_mail(subfolder)
