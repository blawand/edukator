# core/quickslides.py

import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import openai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.conf import settings

# Set up OpenAI API
openai.api_key = settings.OPENAI_API_KEY

# Define the scopes and the credentials file
SCOPES = ['https://www.googleapis.com/auth/presentations']
CREDENTIALS_FILE = os.path.join(settings.BASE_DIR, 'config', 'credentials.json')
TOKEN_FILE = os.path.join(settings.BASE_DIR, 'config', 'token.json')

def get_google_slides_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return build('slides', 'v1', credentials=creds)

def generate_slide_content(topic):
    """Generate slide content using OpenAI GPT"""
    prompt = f"Create a brief outline for a presentation on {topic}. Include 5 main points with short descriptions."
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip().split('\n')

def create_presentation(topic):
    """Create a Google Slides presentation"""
    try:
        service = get_google_slides_service()

        # Create a new presentation
        presentation = service.presentations().create(body={'title': f'Presentation on {topic}'}).execute()
        presentation_id = presentation['presentationId']

        # Generate content
        content = generate_slide_content(topic)

        # Create slides
        requests = []
        for i, point in enumerate(content):
            requests.append({
                'createSlide': {
                    'insertionIndex': str(i),
                    'slideLayoutReference': {
                        'predefinedLayout': 'TITLE_AND_BODY'
                    }
                }
            })

        # Execute the requests
        service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': requests}
        ).execute()

        # Update slide contents
        requests = []
        for i, point in enumerate(content):
            requests.extend([
                {
                    'insertText': {
                        'objectId': f'i{i}',
                        'insertionIndex': 0,
                        'text': point
                    }
                }
            ])

        # Execute the requests
        service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': requests}
        ).execute()

        return f"https://docs.google.com/presentation/d/{presentation_id}/edit"

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

# Add this function to your views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def create_quick_slides(request):
    topic = request.data.get('topic')
    if not topic:
        return Response({'error': 'Topic is required'}, status=400)
    
    presentation_url = create_presentation(topic)
    if presentation_url:
        return Response({'url': presentation_url})
    else:
        return Response({'error': 'Failed to create presentation'}, status=500)