# core/views.py
from django.http import HttpResponse
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.middleware.csrf import get_token
from .serializers import UserSerializer, UploadedFileSerializer
from rest_framework.decorators import api_view
from core.quickslides import create_presentation
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

# Home view for simple response
def home(request):
    return HttpResponse("Welcome to Edukator!")

# User registration view
class UserCreateView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# Logout view
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# CSRF token view
class GetCSRFToken(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        token = get_token(request)
        return Response({'csrftoken': token})

# File upload view
class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = UploadedFileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Function to create quick slides
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

# Custom Auth Token view
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })