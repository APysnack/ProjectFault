from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask import current_app

DOCUMENT_ID = '1-laowzeAnWwbDP_c5q6iB4J2-YTaPz8PGLSYgvCu5Co'


def get_doc_url(is_pdf=False):
    credentials = current_app.config['GOOGLE_DOCS_CREDENTIALS']
    service = build('docs', 'v1', credentials=credentials)
    document = service.documents().get(documentId=DOCUMENT_ID).execute()
    document_url = document['documentId']
    if is_pdf:
        return f'https://docs.google.com/document/d/{document_url}/export?format=pdf'
    else:
        return f'https://docs.google.com/document/d/{document_url}/edit'
