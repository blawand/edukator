# core/utils.py
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings

def get_google_slides_service():
    SCOPES = ['https://www.googleapis.com/auth/presentations']
    credentials = service_account.Credentials.from_service_account_file(
        os.path.join(settings.BASE_DIR, 'path_to_your_service_account.json'), scopes=SCOPES)
    service = build('slides', 'v1', credentials=credentials)
    return service

def create_presentation(title):
    service = get_google_slides_service()
    presentation = {
        'title': title
    }
    presentation = service.presentations().create(body=presentation).execute()
    return presentation

def add_slide(presentation_id, slide_title, slide_content):
    service = get_google_slides_service()
    requests = [
        {
            'createSlide': {
                'objectId': slide_title,
                'insertionIndex': '1',
                'slideLayoutReference': {
                    'predefinedLayout': 'TITLE_AND_BODY'
                }
            }
        },
        {
            'insertText': {
                'objectId': slide_title,
                'insertionIndex': '0',
                'text': slide_content
            }
        }
    ]
    body = {
        'requests': requests
    }
    response = service.presentations().batchUpdate(
        presentationId=presentation_id, body=body).execute()
    return response